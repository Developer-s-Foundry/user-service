from src.utils.svcs import Service
from src.utils.logger import LoggerInterface
from src.api.models.postgres import User, Wallet, UserWithdrawalInformation
from src.api.typing.UserExists import UserExists
from src.api.typing.UserWallet import UserWallet
from src.api.typing.UserSuccess import UserSuccess
from src.api.repositories.UserRepository import UserRepository
from src.api.interfaces.WalletServiceInterface import WalletServiceInterface
from src.api.models.payload.requests.CreateUserRequest import CreateUserRequest
from src.api.models.payload.requests.UpdateUserRequest import UpdateUserRequest
from src.api.models.payload.requests.AuthenticateUserOtp import AuthenticateUserOtp
from src.api.models.payload.requests.CreateWalletRequest import CreateWalletRequest
from src.api.models.payload.requests.AuthenticateUserRequest import (
    AuthenticateUserRequest,
)
from src.api.repositories.UserWithdrawalInformationRepository import (
    UserWithdrawalInformationRepository,
)
from src.api.models.payload.requests.AddWithdrawalAccountRequest import (
    AddWithdrawalAccountRequest,
)

from .UtilityService import UtilityService


@Service()
class UserService:
    def __init__(
        self, log: LoggerInterface, wallet_service: WalletServiceInterface
    ) -> None:
        self.log = log
        self.wallet_service = wallet_service

    async def create(self, req: CreateUserRequest) -> UserExists:
        email = req.email
        password = req.password

        existing_user = await UserRepository.find_by_email(email)
        if existing_user:
            return {"is_exists": True, "user": existing_user}

        hashed_password: str = await UtilityService.hash_string(password)
        req = req.model_copy(update={"password": hashed_password})

        created_user = await UserRepository.add(req)

        user = UtilityService.sanitize_user_object(created_user)

        otp = UtilityService.generate_random_string(length=6, numeric_only=True)
        otp  # Send OTP to user

        return {"is_exists": False, "user": user}

    async def validate_email(self, req: AuthenticateUserOtp) -> bool:
        email = req.email
        otp = req.otp

        user = await UserRepository.find_by_email(email)
        if not user:
            self.log.info("Could not validate user as user does not exist", email, otp)
            return False

        # check otp storage to validate sent otp
        email
        otp

        await UserRepository.update_by_user(
            user, {"is_active": True, "is_enabled": True, "is_validated": True}
        )

        return True

    async def authenticate(self, req: AuthenticateUserRequest) -> UserSuccess:
        email = req.email
        password = req.password

        existing_user = await UserRepository.find_by_email(email)
        if not existing_user:
            return {"is_success": False, "message": "Invalid email or password"}

        is_password_check_ok = await UtilityService.compare_hash(
            password, existing_user.password
        )
        if not is_password_check_ok:
            return {"is_success": False, "message": "Invalid email or password"}

        if not existing_user.is_validated:
            # resend otp
            return {
                "is_success": False,
                "message": "User account not validated. Please check your email for further instructions",
            }

        if not existing_user.is_active:
            return {
                "is_success": False,
                "message": "User account inactive. Please contact support",
            }

        if not existing_user.is_enabled:
            return {
                "is_success": False,
                "message": "User account disabled. Please contact support",
            }

        if not existing_user.is_deleted:
            return {
                "is_success": False,
                "message": "User account has been deleted. Please contact support if you want to restore your account",
            }

        user = UtilityService.sanitize_user_object(existing_user)

        return {"is_success": True, "user": user}

    async def get_user_information(self, id: str) -> User:
        existing_user = await UserRepository.find_by_id(id)
        user = UtilityService.sanitize_user_object(existing_user)
        return user

    async def set_pin(self, id: str, pin: str) -> bool:
        existing_user = await UserRepository.find_by_id(id)
        if existing_user:
            await UserRepository.update_by_user(existing_user, {"pin": pin})
            return True
        return False

    async def update(self, req: UpdateUserRequest) -> UserSuccess:
        id = req.id

        existing_user = await UserRepository.find_by_id(id)
        if not existing_user:
            return {"is_success": False, "message": "User doesn't exist!"}

        updated_user = await UserRepository.update_by_id(
            id, req.model_dump(exclude={"id"})
        )
        user = UtilityService.sanitize_user_object(updated_user)

        return {"is_success": True, "user": user}

    async def add_withdrawal_account(
        self,
        req: AddWithdrawalAccountRequest,
    ) -> UserWithdrawalInformation:
        withdrawal_information = await UserWithdrawalInformationRepository.add(req)
        return withdrawal_information

    async def update_withdrawal_account(
        self,
        id: int,
        req: AddWithdrawalAccountRequest,
    ) -> None:
        await UserWithdrawalInformationRepository.update_user_account(
            id, req.model_dump(exclude_unset=True)
        )

    async def delete_withdrawal_account(self, id: int) -> None:
        await UserWithdrawalInformationRepository.delete_user_withdrawal_account(id)

    # ********** Wallet **********

    async def create_wallet(self, req: CreateWalletRequest) -> UserWallet:
        user = await self.get_user_information(req.user)
        req.tier = user.tier

        wallet = await self.wallet_service.create_wallet(req)

        return {"user": user, "wallet": wallet}

    async def list_wallets(self, user_id: str) -> list[Wallet]:
        wallets = await self.wallet_service.list_wallets(user_id)
        return wallets

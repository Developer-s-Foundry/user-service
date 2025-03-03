from src.utils.svcs import Service
from src.utils.logger import LoggerInterface
from src.api.models.postgres import User, UserWithdrawalInformation
from src.api.typing.UserExists import UserExists
from src.api.typing.UserSuccess import UserSuccess
from src.api.repositories.UserRepository import UserRepository
from src.api.models.serializers.requests.CreateUserRequest import CreateUserRequest
from src.api.models.serializers.requests.UpdateUserRequest import UpdateUserRequest
from src.api.models.serializers.requests.AuthenticateUserOtp import AuthenticateUserOtp
from src.api.repositories.UserWithdrawalInformationRepository import (
    UserWithdrawalInformationRepository,
)
from src.api.models.serializers.requests.AuthenticateUserRequest import (
    AuthenticateUserRequest,
)
from src.api.models.serializers.requests.AddWithdrawalAccountRequest import (
    AddWithdrawalAccountRequest,
)

from .UtilityService import UtilityService


@Service()
class UserService:
    def __init__(self, log: LoggerInterface) -> None:
        self.log = log

    async def create(self, req: CreateUserRequest) -> UserExists:
        data = req.validated_data
        email: str = data["email"]
        password: str = data["password"]

        existing_user = await UserRepository.find_by_email(email)
        if existing_user:
            return {"is_exists": True, "user": existing_user}

        hashed_password: str = await UtilityService.hash_string(password)

        data.update(password=hashed_password)
        created_user = await UserRepository.add(User(**data))

        user = UtilityService.sanitize_user_object(created_user)

        otp = UtilityService.generate_random_string(length=6, numeric_only=True)
        otp  # Send OTP to user

        return {"is_exists": False, "user": user}

    async def validate_email(self, req: AuthenticateUserOtp) -> bool:
        email: str = req.validated_data["email"]
        otp: str = req.validated_data["otp"]

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
        email: str = req.validated_data["email"]
        password: str = req.validated_data["password"]

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

    async def get_user_information(id: str) -> User:
        existing_user = await UserRepository.find_by_id(id)
        user = UtilityService.sanitize_user_object(existing_user)
        return user

    async def set_pin(id: str, pin: str) -> bool:
        existing_user = await UserRepository.find_by_id(id)
        await UserRepository.update_by_user(existing_user, {"pin": pin})
        return True

    async def update(self, req: UpdateUserRequest) -> UserSuccess:
        data = req.validated_data
        id: str = data["id"]

        existing_user = await UserRepository.find_by_id(id)
        if not existing_user:
            return {"is_success": False, "message": "User doesn't exist!"}

        updated_user = await UserRepository.update_by_id(id, data)
        user = UtilityService.sanitize_user_object(updated_user)

        return {"is_success": True, "user": user}

    async def add_withdrawal_account(
        req: AddWithdrawalAccountRequest,
    ) -> UserWithdrawalInformation:
        data = req.validated_data
        withdrawal_information = await UserWithdrawalInformationRepository.add(
            UserWithdrawalInformation(**data)
        )
        return withdrawal_information

    async def update_withdrawal_account(
        id: int,
        req: AddWithdrawalAccountRequest,
    ) -> None:
        data = req.validated_data
        await UserWithdrawalInformationRepository.update_user_account(id, data)

    async def delete_withdrawal_account(id: int) -> None:
        await UserWithdrawalInformationRepository.delete_user_withdrawal_account(id)

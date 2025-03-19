from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.models.postgres import User, Wallet
from src.api.typing.UserWallet import UserWallet
from src.api.typing.UserSuccess import UserSuccess
from src.api.repositories.UserRepository import UserRepository
from src.api.models.payload.requests.UpdateUserRequest import UpdateUserRequest
from src.api.models.payload.requests.CreateWalletRequest import CreateWalletRequest

from .WalletService import WalletService
from .UtilityService import UtilityService


@Service()
class UserService:
    def __init__(
        self,
        logger: Logger,
        utility_service: UtilityService,
        wallet_service: WalletService,
    ) -> None:
        self.logger = logger
        self.utility_service = utility_service
        self.wallet_service = wallet_service

    async def get_user_information(self, id: str) -> User:
        existing_user = await UserRepository.find_by_id(id)
        user = self.utility_service.sanitize_user_object(existing_user)
        return user

    async def set_pin(self, id: str, pin: str) -> UserSuccess:
        existing_user = await UserRepository.find_by_id(id)
        if not existing_user:
            return {"is_success": False, "message": "User doesn't exist!"}
        if existing_user.pin:
            return {
                "is_success": False,
                "message": "You already have a transaction PIN on your account!",
            }
        await UserRepository.update_by_user(existing_user, {"pin": pin})
        return {"is_success": True, "message": "Transaction PIN created!"}

    async def update(self, req: UpdateUserRequest) -> UserSuccess:
        id = req._id

        existing_user = await UserRepository.find_by_id(id)
        if not existing_user:
            return {"is_success": False, "message": "User doesn't exist!"}

        updated_user = await UserRepository.update_by_id(
            id, req.model_dump(exclude_unset=True)
        )
        user = self.utility_service.sanitize_user_object(updated_user)

        return {"is_success": True, "user": user}

    # ********** Wallet **********

    async def create_wallet(self, req: CreateWalletRequest) -> UserWallet:
        user = await self.get_user_information(req.user)
        req.tier = user.tier

        wallet = await self.wallet_service.create_wallet(req)

        return {"user": user, "wallet": wallet}

    async def list_wallets(self, user_id: str) -> list[Wallet]:
        wallets = await self.wallet_service.list_wallets(user_id)
        return wallets

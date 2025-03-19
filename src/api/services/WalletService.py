from src.utils.svcs import Service
from src.api.models.postgres import Wallet
from src.api.repositories.WalletRepository import WalletRepository
from src.api.repositories.WalletLimitRepository import WalletLimitRepository
from src.api.models.payload.requests.CreateWalletRequest import CreateWalletRequest


@Service()
class WalletService:
    async def __generate_account_number(self) -> str:
        total_number_of_existing_accounts = await WalletRepository.count()
        generated_account_number = f"{10000000001 + total_number_of_existing_accounts}"
        return generated_account_number

    async def __get_user_account_limit(self, tier: int) -> float:
        account_limit = await WalletLimitRepository.find_by_tier(tier)
        if not account_limit:
            raise ValueError("Account limit for this tier does not exist")
        return account_limit.daily_transaction_limit

    async def create_wallet(self, req: CreateWalletRequest) -> Wallet:
        account_number = await self.__generate_account_number()
        account_limit = await self.__get_user_account_limit(req.tier)

        req = req.model_copy(
            update={
                "account_number": account_number,
                "daily_transaction_limit": account_limit,
            }
        )
        wallet = await WalletRepository.add(req)
        return wallet

    async def list_wallets(self, user_id: str) -> list[Wallet]:
        wallets = await WalletRepository.list({"user__id": user_id})
        return wallets

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.models.postgres import UserWithdrawalInformation
from src.api.typing.AccountSuccess import AccountSuccess
from src.api.repositories.UserRepository import UserRepository
from src.api.repositories.UserWithdrawalInformationRepository import (
    UserWithdrawalInformationRepository,
)
from src.api.models.payload.requests.AddWithdrawalAccountRequest import (
    AddWithdrawalAccountRequest,
)


@Service()
class WithdrawalAccountService:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    async def add_withdrawal_account(
        self,
        user_id: str,
        req: AddWithdrawalAccountRequest,
    ) -> AccountSuccess:
        user = await UserRepository.find_by_id(user_id)
        if not user:
            raise ValueError("User does not exists")
        account_already_exists = (
            await UserWithdrawalInformationRepository.find_by_account_number(
                req.account_number
            )
        )
        if account_already_exists:
            return {
                "is_success": False,
                "message": f"You already have an account with the account number {req.account_number}!",
                "account": account_already_exists,
            }
        withdrawal_information = await UserWithdrawalInformationRepository.add(
            user, req
        )
        return {
            "is_success": True,
            "message": "Withdrawal account details saved succesfully",
            "account": withdrawal_information,
        }

    async def update_withdrawal_account(
        self,
        user_id: str,
        id: int,
        req: AddWithdrawalAccountRequest,
    ) -> None:
        user = await UserRepository.find_by_id(user_id)
        if not user:
            raise ValueError("User does not exists")
        await UserWithdrawalInformationRepository.update_user_account(
            user, id, req.model_dump(exclude_unset=True)
        )

    async def get_withdrawal_account(self, user_id: str, id: int) -> AccountSuccess:
        withdrawal_account = await UserWithdrawalInformationRepository.find_by_id(id)
        if not withdrawal_account:
            return {"is_success": False, "message": "Account not found!"}

        if withdrawal_account.user.id != user_id:  # type: ignore
            return {"is_success": False, "message": "Unauthorized request!"}

        return {"is_success": True, "account": withdrawal_account}

    async def fetch_withdrawal_accounts(
        self, user_id: str
    ) -> list[UserWithdrawalInformation]:
        withdrawal_accounts = await UserWithdrawalInformationRepository.list(user_id)
        return withdrawal_accounts

    async def delete_withdrawal_account(self, user_id: str, id: int) -> AccountSuccess:
        account_already_exists = await UserWithdrawalInformationRepository.find_by_id(
            id
        )
        if not account_already_exists:
            return {"is_success": False, "message": "Account not found!"}

        if account_already_exists.user.id != user_id:  # type: ignore
            return {"is_success": False, "message": "Unauthorized request!"}

        await UserWithdrawalInformationRepository.delete_user_withdrawal_account(id)
        return {
            "is_success": True,
            "message": "Withdrawal account successfully deleted!",
        }

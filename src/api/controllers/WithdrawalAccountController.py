from http import HTTPStatus

from ninja.errors import HttpError

from src.utils.svcs import Service
from src.api.models.postgres import UserWithdrawalInformation
from src.api.services.WithdrawalAccountService import WithdrawalAccountService
from src.api.models.payload.requests.AddWithdrawalAccountRequest import (
    AddWithdrawalAccountRequest,
)


@Service()
class WithdrawalAccountController:
    def __init__(self, withdraw_service: WithdrawalAccountService) -> None:
        self.withdraw_service = withdraw_service

    async def add_withdrawal_account(
        self, user_id: str, account_data: AddWithdrawalAccountRequest
    ) -> tuple:
        created_wallet = await self.withdraw_service.add_withdrawal_account(
            user_id, account_data
        )
        if created_wallet["is_success"]:
            return HTTPStatus.CREATED, {"message": created_wallet["message"]}
        raise HttpError(HTTPStatus.BAD_REQUEST, created_wallet["message"])

    async def list_withdrawal_accounts(
        self, user_id: str
    ) -> list[UserWithdrawalInformation]:
        withdrawal_accounts = await self.withdraw_service.fetch_withdrawal_accounts(
            user_id
        )
        return withdrawal_accounts

    async def delete_withdrawal_account(self, user_id: str, id: int) -> dict:
        withdrawal_account_deleted = (
            await self.withdraw_service.delete_withdrawal_account(user_id, id)
        )
        if not withdrawal_account_deleted["is_success"]:
            raise HttpError(HTTPStatus.FORBIDDEN, withdrawal_account_deleted["message"])
        return {"message": withdrawal_account_deleted["message"]}

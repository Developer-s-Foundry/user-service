from http import HTTPStatus
from typing import Annotated

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.utils.response_format import error_response, success_response
from src.api.services.WithdrawalAccountService import WithdrawalAccountService
from src.api.models.payload.requests.AddWithdrawalAccountRequest import (
    AddWithdrawalAccountRequest,
)


@Service()
class WithdrawalAccountController:
    def __init__(
        self,
        logger: Annotated[Logger, "WithdrawalAccountController"],
        withdraw_service: WithdrawalAccountService,
    ) -> None:
        self.logger = logger
        self.withdraw_service = withdraw_service

    async def add_withdrawal_account(
        self, user_id: str, account_data: AddWithdrawalAccountRequest
    ) -> dict:
        created_wallet = await self.withdraw_service.add_withdrawal_account(
            user_id, account_data
        )
        if created_wallet["is_success"]:
            return success_response(
                message=created_wallet["message"], status_code=HTTPStatus.CREATED
            )
        return error_response(
            message=created_wallet["message"], status_code=HTTPStatus.BAD_REQUEST
        )

    async def list_withdrawal_accounts(self, user_id: str) -> dict:
        withdrawal_accounts = await self.withdraw_service.fetch_withdrawal_accounts(
            user_id
        )
        return success_response(
            message="Successfully retrieved wallets",
            data=withdrawal_accounts,
            status_code=HTTPStatus.OK,
        )

    async def get_withdrawal_account(self, user_id: str, id: int) -> dict:
        withdrawal_account = await self.withdraw_service.get_withdrawal_account(
            user_id, id
        )
        if not withdrawal_account["is_success"]:
            return error_response(
                message=withdrawal_account["message"],
                status_code=HTTPStatus.NOT_FOUND,
            )
        return success_response(
            message="Successfully retrieved account",
            data=withdrawal_account["account"],
            status_code=HTTPStatus.OK,
        )

    async def delete_withdrawal_account(self, user_id: str, id: int) -> dict:
        withdrawal_account_deleted = (
            await self.withdraw_service.delete_withdrawal_account(user_id, id)
        )
        if not withdrawal_account_deleted["is_success"]:
            return error_response(
                message=withdrawal_account_deleted["message"],
                status_code=HTTPStatus.FORBIDDEN,
            )
        return success_response(
            message=withdrawal_account_deleted["message"], status_code=HTTPStatus.OK
        )

from http import HTTPStatus
from typing import Annotated

from ninja.errors import HttpError

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.models.postgres import UserWithdrawalInformation
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
    ) -> tuple:
        try:
            created_wallet = await self.withdraw_service.add_withdrawal_account(
                user_id, account_data
            )
            if created_wallet["is_success"]:
                return HTTPStatus.CREATED, {"message": created_wallet["message"]}
            raise HttpError(HTTPStatus.BAD_REQUEST, created_wallet["message"])
        except Exception as exc:
            if isinstance(exc, HttpError):
                raise
            self.logger.error(
                {
                    "activity_type": "Add withdraw account",
                    "message": str(exc),
                    "metadata": {
                        "user": {"id": user_id},
                        "account_data": account_data.model_dump(),
                    },
                }
            )
            raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")

    async def list_withdrawal_accounts(
        self, user_id: str
    ) -> list[UserWithdrawalInformation]:
        try:
            withdrawal_accounts = await self.withdraw_service.fetch_withdrawal_accounts(
                user_id
            )
            return withdrawal_accounts
        except Exception as exc:
            if isinstance(exc, HttpError):
                raise
            self.logger.error(
                {
                    "activity_type": "List withdraw accounts",
                    "message": str(exc),
                    "metadata": {"user": {"id": user_id}},
                }
            )
            raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")

    async def get_withdrawal_account(
        self, user_id: str, id: int
    ) -> UserWithdrawalInformation:
        try:
            withdrawal_account = await self.withdraw_service.get_withdrawal_account(
                user_id, id
            )
            if not withdrawal_account["is_success"]:
                raise HttpError(HTTPStatus.NOT_FOUND, withdrawal_account["message"])
            return withdrawal_account["account"]
        except Exception as exc:
            if isinstance(exc, HttpError):
                raise
            self.logger.error(
                {
                    "activity_type": "Get withdraw account",
                    "message": str(exc),
                    "metadata": {"user": {"id": user_id}, "accounta": {"id": id}},
                }
            )
            raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")

    async def delete_withdrawal_account(self, user_id: str, id: int) -> dict:
        try:
            withdrawal_account_deleted = (
                await self.withdraw_service.delete_withdrawal_account(user_id, id)
            )
            if not withdrawal_account_deleted["is_success"]:
                raise HttpError(
                    HTTPStatus.FORBIDDEN, withdrawal_account_deleted["message"]
                )
            return {"message": withdrawal_account_deleted["message"]}
        except Exception as exc:
            if isinstance(exc, HttpError):
                raise
            self.logger.error(
                {
                    "activity_type": "Delete withdraw account",
                    "message": str(exc),
                    "metadata": {"user": {"id": user_id}, "accounta": {"id": id}},
                }
            )
            raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")

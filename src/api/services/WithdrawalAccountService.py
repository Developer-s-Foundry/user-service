from typing import Annotated

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.models.postgres import UserWithdrawalInformation
from src.api.typing.AccountSuccess import AccountSuccess
from src.api.constants.activity_types import ACTIVITY_TYPES
from src.api.repositories.UserRepository import UserRepository
from src.api.repositories.UserWithdrawalInformationRepository import (
    UserWithdrawalInformationRepository,
)
from src.api.models.payload.requests.AddWithdrawalAccountRequest import (
    AddWithdrawalAccountRequest,
)


@Service()
class WithdrawalAccountService:
    def __init__(self, logger: Annotated[Logger, "WithdrawalAccountService"]) -> None:
        self.logger = logger

    async def add_withdrawal_account(
        self,
        user_id: str,
        req: AddWithdrawalAccountRequest,
    ) -> AccountSuccess:
        user = await UserRepository.find_by_id(user_id)
        if not user:
            message = "User does not exists"
            self.logger.warn(
                {
                    "activity_type": ACTIVITY_TYPES["ADD_WITHDRAW_ACCOUNT"],
                    "message": message,
                    "metadata": {"user": {"id": user_id}},
                }
            )
            raise ValueError(message)
        account_already_exists = (
            await UserWithdrawalInformationRepository.find_by_account_number(
                req.account_number
            )
        )
        if account_already_exists:
            message = f"You already have an account with the account number {req.account_number}!"
            self.logger.info(
                {
                    "activity_type": ACTIVITY_TYPES["ADD_WITHDRAW_ACCOUNT"],
                    "message": message,
                    "metadata": {"user": {"id": user_id}, "account": req.model_dump()},
                }
            )
            return {
                "is_success": False,
                "message": message,
                "account": account_already_exists,
            }
        withdrawal_information = await UserWithdrawalInformationRepository.add(
            user, req
        )

        message = "Withdrawal account details saved succesfully"
        self.logger.info(
            {
                "activity_type": ACTIVITY_TYPES["ADD_WITHDRAW_ACCOUNT"],
                "message": message,
                "metadata": {"user": {"id": user_id}, "account": req.model_dump()},
            }
        )
        return {
            "is_success": True,
            "message": message,
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
            message = "User does not exists"
            self.logger.warn(
                {
                    "activity_type": "Update withdraw account",
                    "message": message,
                    "metadata": {"user": {"id": user_id}},
                }
            )
            raise ValueError(message)
        await UserWithdrawalInformationRepository.update_user_account(
            user, id, req.model_dump(exclude_unset=True)
        )
        self.logger.info(
            {
                "activity_type": "Update withdraw account",
                "message": "User Withdraw account updated successfully",
                "metadata": {
                    "user": {"id": user_id},
                    "account": dict(id=id, **req.model_dump()),
                },
            }
        )

    async def get_withdrawal_account(self, user_id: str, id: int) -> AccountSuccess:
        withdrawal_account = await UserWithdrawalInformationRepository.find_by_id(id)
        if not withdrawal_account:
            message = "Account not found!"
            self.logger.info(
                {
                    "activity_type": ACTIVITY_TYPES["FETCH_WITHDRAW_ACCOUNT"],
                    "message": message,
                    "metadata": {
                        "user": {"id": user_id},
                        "account": {"id": id},
                    },
                }
            )
            return {"is_success": False, "message": message}

        if withdrawal_account.user.id != user_id:
            message = "Unauthorized request!"
            self.logger.warn(
                {
                    "activity_type": ACTIVITY_TYPES["FETCH_WITHDRAW_ACCOUNT"],
                    "message": message,
                    "metadata": {
                        "user": {"id": user_id},
                        "account": {"id": id, "user_id": withdrawal_account.user.id},
                    },
                }
            )
            return {"is_success": False, "message": message}

        self.logger.info(
            {
                "activity_type": ACTIVITY_TYPES["FETCH_WITHDRAW_ACCOUNT"],
                "message": "User Account fetched successfully",
                "metadata": {
                    "user": {"id": user_id},
                    "account": {"id": id},
                },
            }
        )
        return {"is_success": True, "account": withdrawal_account}

    async def fetch_withdrawal_accounts(
        self, user_id: str
    ) -> list[UserWithdrawalInformation]:
        withdrawal_accounts = await UserWithdrawalInformationRepository.list(user_id)
        self.logger.info(
            {
                "activity_type": ACTIVITY_TYPES["LIST_WITHDRAW_ACCOUNTS"],
                "message": "User Accounts fetched successfully",
                "metadata": {"user": {"id": user_id}},
            }
        )
        return withdrawal_accounts

    async def delete_withdrawal_account(self, user_id: str, id: int) -> AccountSuccess:
        account_already_exists = await UserWithdrawalInformationRepository.find_by_id(
            id
        )
        if not account_already_exists:
            message = "Account not found!"
            self.logger.info(
                {
                    "activity_type": ACTIVITY_TYPES["DELETE_WITHDRAW_ACCOUNT"],
                    "message": message,
                    "metadata": {
                        "user": {"id": user_id},
                        "account": {"id": id},
                    },
                }
            )
            return {"is_success": False, "message": message}

        if account_already_exists.user.id != user_id:
            message = "Unauthorized request!"
            self.logger.warn(
                {
                    "activity_type": ACTIVITY_TYPES["DELETE_WITHDRAW_ACCOUNT"],
                    "message": message,
                    "metadata": {
                        "user": {"id": user_id},
                        "account": {
                            "id": id,
                            "user_id": account_already_exists.user.id,
                        },
                    },
                }
            )
            return {"is_success": False, "message": message}

        await UserWithdrawalInformationRepository.delete_user_withdrawal_account(id)

        message = "Withdrawal account successfully deleted!"
        self.logger.info(
            {
                "activity_type": ACTIVITY_TYPES["DELETE_WITHDRAW_ACCOUNT"],
                "message": message,
                "metadata": {
                    "user": {"id": user_id},
                    "account": {"id": id},
                },
            }
        )
        return {"is_success": True, "message": message}

from typing import TypedDict, NotRequired

from src.api.models.postgres import UserWithdrawalInformation


class AccountSuccess(TypedDict):
    is_success: bool
    message: NotRequired[str]
    account: NotRequired[UserWithdrawalInformation]

from typing import TypedDict, NotRequired

from src.api.models.postgres import User


class UserSuccess(TypedDict):
    is_success: bool
    message: NotRequired[str]
    user: NotRequired[User]
    token: NotRequired[str]

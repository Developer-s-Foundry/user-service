from typing import TypedDict, NotRequired

from src.api.models.postgres import User


class UserExists(TypedDict):
    is_exists: bool
    user: NotRequired[User]

from typing import TypedDict

from src.api.models.postgres import User


class UserExists(TypedDict):
    is_exists: bool
    user: User
    message: str

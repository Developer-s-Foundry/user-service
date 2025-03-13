from typing import TypedDict

from src.api.models.postgres import User, Wallet


class UserWallet(TypedDict):
    user: User
    wallet: Wallet

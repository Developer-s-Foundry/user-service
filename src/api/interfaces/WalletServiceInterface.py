from typing import Protocol

from src.api.models.postgres import Wallet
from src.api.models.payload.requests.CreateWalletRequest import CreateWalletRequest


class WalletServiceInterface(Protocol):
    async def create_wallet(self, req: CreateWalletRequest) -> Wallet: ...

    async def list_wallets(self, user_id: str) -> list[Wallet]: ...

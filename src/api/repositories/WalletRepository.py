from src.api.models.postgres import Wallet
from src.api.models.payload.requests.CreateWalletRequest import CreateWalletRequest

from ._base import BaseRepository


class WalletRepository(BaseRepository[Wallet]):
    model = Wallet

    @classmethod
    async def add(cls, wallet_data: CreateWalletRequest) -> Wallet:
        return await cls.manager.acreate(
            **wallet_data.model_dump(exclude_none=True, exclude_unset=True)
        )

    @classmethod
    async def find_by_id(cls, id: int) -> Wallet | None:
        return await cls.manager.filter(id=id).afirst()

    @classmethod
    async def list(cls, filter: dict = {}) -> list[Wallet]:
        return [wallet async for wallet in cls.manager.filter(**filter).order_by("id")]

    @classmethod
    async def update_wallet(cls, id: int, updates: dict | None = None) -> None:
        wallet = await WalletRepository.find_by_id(id)

        if wallet and updates:
            for key, value in updates.items():
                setattr(wallet, key, value)
            await wallet.asave()

    @classmethod
    async def delete_wallet(cls, id: int) -> None:
        wallet = await WalletRepository.find_by_id(id)
        if wallet:
            await wallet.adelete()

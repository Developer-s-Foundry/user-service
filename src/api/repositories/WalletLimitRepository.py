from src.api.models.postgres import WalletLimit

from ._base import BaseRepository


class WalletLimitRepository(BaseRepository[WalletLimit]):
    model = WalletLimit

    @classmethod
    async def add(cls, wallet_limit_data: dict) -> WalletLimit:
        return await cls.manager.acreate(**wallet_limit_data)

    @classmethod
    async def find_by_id(cls, id: int) -> WalletLimit | None:
        return await cls.manager.filter(id=id).afirst()

    @classmethod
    async def find_by_tier(cls, tier: int) -> WalletLimit | None:
        return await cls.manager.filter(tier=tier).afirst()

    @classmethod
    async def list(cls) -> list[WalletLimit]:
        return [limit async for limit in cls.manager.order_by("id")]

    @classmethod
    async def update_wallet_limit(cls, id: int, updates: dict | None = None) -> None:
        limit = await WalletLimitRepository.find_by_id(id)

        if limit and updates:
            for key, value in updates.items():
                setattr(limit, key, value)
            await limit.asave()

    @classmethod
    async def delete_wallet_limit(cls, id: int) -> None:
        limit = await WalletLimitRepository.find_by_id(id)
        if limit:
            await limit.adelete()

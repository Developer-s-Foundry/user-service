from src.api.models.postgres import User, UserWithdrawalInformation
from src.api.models.payload.requests.AddWithdrawalAccountRequest import (
    AddWithdrawalAccountRequest,
)

from ._base import BaseRepository


class UserWithdrawalInformationRepository(BaseRepository[UserWithdrawalInformation]):
    model = UserWithdrawalInformation

    @classmethod
    async def add(
        cls, user: User, user_account_data: AddWithdrawalAccountRequest
    ) -> UserWithdrawalInformation:
        return await cls.manager.acreate(user=user, **user_account_data.model_dump())

    @classmethod
    async def find_by_id(cls, id: int) -> UserWithdrawalInformation | None:
        return await cls.manager.filter(id=id).afirst()

    @classmethod
    async def find_by_user_and_id(
        cls, user_id: str, id: int
    ) -> UserWithdrawalInformation | None:
        return await cls.manager.filter(user__id=user_id, id=id).afirst()

    @classmethod
    async def find_by_account_number(
        cls, account_number: str
    ) -> UserWithdrawalInformation | None:
        return await cls.manager.filter(account_number=account_number).afirst()

    @classmethod
    async def list(cls, user_id: str) -> list[UserWithdrawalInformation]:
        return [info async for info in cls.manager.filter(user__id=user_id)]

    @classmethod
    async def update_user_account(
        cls, user: User, user_account_id: int, updates: dict | None = None
    ) -> None:
        user_account = await UserWithdrawalInformationRepository.find_by_id(
            user_account_id
        )

        if user_account and updates:
            for key, value in updates.items():
                setattr(user_account, key, value)
            await user_account.asave()

    @classmethod
    async def delete_user_withdrawal_account(cls, account_id: int) -> None:
        account = await UserWithdrawalInformationRepository.find_by_id(account_id)
        if account:
            await account.adelete()

from src.api.models.postgres import User
from src.api.models.payload.requests.CreateUserRequest import CreateUserRequest

from ._base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    @classmethod
    async def add(cls, user_data: CreateUserRequest) -> User:
        return await cls.manager.acreate(**user_data.model_dump())

    @classmethod
    async def find_by_id(cls, id: str) -> User | None:
        return await cls.manager.filter(id=id).afirst()

    @classmethod
    async def find_by_email(cls, email: str) -> User | None:
        return await cls.manager.filter(email=email).afirst()

    @classmethod
    async def list(cls, filter: dict = {}) -> list[User]:
        return [user async for user in cls.manager.filter(**filter)]

    @classmethod
    async def update_by_user(cls, user: User, updates: dict | None = None) -> User:
        if updates:
            for key, value in updates.items():
                setattr(user, key, value)
            await user.asave()
        return user

    @classmethod
    async def update_by_id(cls, id: str, updates: dict | None = None) -> User | None:
        user = await UserRepository.find_by_id(id)
        if user and updates:
            for key, value in updates.items():
                setattr(user, key, value)
            await user.asave()
        return user

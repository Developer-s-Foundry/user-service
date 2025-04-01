from src.api.models.postgres import User, UserNextOfKin
from src.api.models.payload.requests.UserNOKRequest import UserNOKRequest

from ._base import BaseRepository


class UserNOKRepository(BaseRepository[UserNextOfKin]):
    model = UserNextOfKin

    @classmethod
    async def add(cls, user: User, nok_details: UserNOKRequest) -> UserNextOfKin:
        return await cls.manager.acreate(
            user=user, **nok_details.model_dump(exclude_unset=True)
        )

    @classmethod
    async def find_by_user(cls, user: User) -> UserNextOfKin | None:
        return await cls.manager.filter(user=user).afirst()

    @classmethod
    async def update(
        cls, nok: UserNextOfKin, nok_details: UserNOKRequest
    ) -> UserNextOfKin:
        for attr, value in nok_details.model_dump(exclude_unset=True).items():
            setattr(nok, attr, value)
        await nok.asave()
        return nok

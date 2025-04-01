from datetime import timedelta

from django.utils import timezone

from src.api.models.postgres import Otp, User

from ._base import BaseRepository


class OtpRepository(BaseRepository[Otp]):
    model = Otp

    @classmethod
    async def add(cls, key: str, user: User | None = None) -> Otp:
        return await cls.manager.acreate(key=key, user=user)

    @classmethod
    async def find_by_key(cls, key: str) -> Otp | None:
        return await cls.manager.filter(key=key).afirst()

    @classmethod
    async def find_valid_key(cls, key: str, lifetime: timedelta) -> Otp | None:
        return await cls.manager.filter(
            key=key, created_at__gte=timezone.now() - lifetime
        ).afirst()

    @classmethod
    async def find_valid_user_key(cls, user: User, lifetime: timedelta) -> Otp | None:
        return await cls.manager.filter(
            user=user, created_at__gte=timezone.now() - lifetime
        ).afirst()

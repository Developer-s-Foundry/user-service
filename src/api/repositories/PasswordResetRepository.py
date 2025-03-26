from uuid import UUID
from datetime import datetime

from src.api.models.postgres import User

from ._base import BaseRepository


class PasswordResetRepository(BaseRepository[User]):
    model = User

    @classmethod
    async def set_new_password_reset_token(
        cls, user: User, token: UUID, expires_at: datetime
    ) -> None:
        user.password_reset_token = token
        user.token_expires_at = expires_at
        await user.asave()

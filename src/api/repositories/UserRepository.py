from ..models.postgres.User import User


class UserRepository:
    async def add(self, user: User) -> User:
        await user.asave()
        return user

    async def find_by_id(self, id: str) -> User:
        return await User.objects.filter(id=id).afirst()

    async def find_by_email(self, email: str) -> User:
        return await User.objects.filter(email=email).afirst()

    async def list(self, filter: dict = {}) -> list[User]:
        return await list(User.objects.filter(**filter))

    async def update_by_user(self, user: User, updates: dict | None = None) -> User:
        if updates:
            for key, value in updates.items():
                setattr(user, key, value)
            await user.asave()
        return user

    async def update_by_id(self, id: str, updates: dict | None = None) -> User:
        user: User | None = User.objects.filter(id=id).afirst()
        if user and updates:
            for key, value in updates.items():
                setattr(user, key, value)
            await user.asave()
        return user

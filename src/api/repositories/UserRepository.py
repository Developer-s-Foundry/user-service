from ..models.postgres import User


class UserRepository:
    @staticmethod
    async def add(user: User) -> User:
        await user.asave()
        return user

    @staticmethod
    async def find_by_id(id: str) -> User | None:
        return await User.objects.filter(id=id).afirst()

    @staticmethod
    async def find_by_email(email: str) -> User | None:
        return await User.objects.filter(email=email).afirst()

    @staticmethod
    async def list(filter: dict = {}) -> list[User]:
        return await list(User.objects.filter(**filter))

    @staticmethod
    async def update_by_user(user: User, updates: dict | None = None) -> User:
        if updates:
            for key, value in updates.items():
                setattr(user, key, value)
            await user.asave()
        return user

    @staticmethod
    async def update_by_id(id: str, updates: dict | None = None) -> User:
        user = await UserRepository.find_by_id(id)
        if user and updates:
            for key, value in updates.items():
                setattr(user, key, value)
            await user.asave()
        return user

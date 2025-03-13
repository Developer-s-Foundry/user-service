from typing import Generic, TypeVar

from django.db.models import Model, Manager

T = TypeVar("T", bound=Model)


class BaseRepository(Generic[T]):
    model: type[T]
    manager: Manager[T]

    def __init_subclass__(cls, **kwargs: dict) -> None:
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "model"):
            raise NotImplementedError(f"{cls.__name__}: model is not defined")

        cls.manager = cls.model.objects

    @classmethod
    async def count(cls, filters: dict = {}) -> int:
        return await cls.manager.filter(**filters).acount()

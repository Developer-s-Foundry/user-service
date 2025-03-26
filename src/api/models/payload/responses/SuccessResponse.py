from typing import Generic, TypeVar

from ninja import Schema

T = TypeVar("T")


class SuccessResponse(Schema, Generic[T]):
    status_code: int
    message: str
    data: T | None = None

from typing import Generic, TypeVar

from ninja import Schema

T = TypeVar("T")


class ErrorResponse(Schema, Generic[T]):
    status_code: int
    message: str
    errors: T | None = None


class ServerErrorResponse(Schema, Generic[T]):
    status_code: int
    message: str
    errors: T | None = None

from typing import Annotated

from pydantic import Field, BaseModel

from src.api.typing.PasswordValidator import IsStrongPassword


class UpdateUserRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    phone_number: str | None = None
    state_lga_id: Annotated[int, Field(default=None, ge=1)]


class ChangeUserPasswordRequest(BaseModel):
    old_password: str
    new_password: IsStrongPassword

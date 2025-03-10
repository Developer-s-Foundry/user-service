from typing import Annotated

from pydantic import Field, EmailStr, BaseModel

from src.api.typing.PasswordValidator import IsStrongPassword


class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: IsStrongPassword
    address: str
    phone_number: str
    state_lga_id: Annotated[int, Field(min_value=1)]

from pydantic import EmailStr, BaseModel

from src.api.typing.PasswordValidator import IsStrongPassword


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: IsStrongPassword

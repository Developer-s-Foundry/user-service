from pydantic import EmailStr, BaseModel

from src.api.typing.PasswordValidator import IsStrongPassword


class AuthenticateUserRequest(BaseModel):
    email: EmailStr
    password: IsStrongPassword

from pydantic import BaseModel

from src.api.typing.PasswordValidator import IsStrongPassword


class AuthenticateUserRequest(BaseModel):
    email: str
    password: IsStrongPassword

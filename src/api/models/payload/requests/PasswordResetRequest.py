from pydantic import EmailStr, BaseModel


class PasswordResetRequest(BaseModel):
    email: EmailStr

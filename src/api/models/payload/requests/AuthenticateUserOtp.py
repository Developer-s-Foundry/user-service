from pydantic import EmailStr, BaseModel


class AuthenticateUserOtp(BaseModel):
    email: EmailStr
    otp: str

from pydantic import BaseModel


class AuthenticateUserOtp(BaseModel):
    email: str
    otp: str

from pydantic import EmailStr, BaseModel


class ResendUserOtp(BaseModel):
    email: EmailStr

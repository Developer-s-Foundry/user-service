from pydantic import EmailStr, BaseModel


class CreateUserRequest(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    address: str
    phone_number: str
    profile_picture: str
    pin: str

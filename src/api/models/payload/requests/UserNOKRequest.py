from pydantic import EmailStr, BaseModel

from src.api.enums.NextOfKinRelationship import NextOfKinRelationship


class UserNOKRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
    relationship: NextOfKinRelationship | None = None

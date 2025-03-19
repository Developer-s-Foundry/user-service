from typing import Annotated

from pydantic import Field, BaseModel


class UpdateUserRequest(BaseModel):
    _id: str
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    phone_number: str | None = None
    state_lga_id: Annotated[int, Field(default=None, ge=1)]

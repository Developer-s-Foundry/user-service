from typing import Annotated

from pydantic import Field, BaseModel


class UpdateUserRequest(BaseModel):
    id: str
    first_name: str
    last_name: str
    address: str
    phone_number: str
    state_lga_id: Annotated[int, Field(min_value=1)]

from pydantic import BaseModel


class Pin(BaseModel):
    pin: str

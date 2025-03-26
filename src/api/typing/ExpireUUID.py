from uuid import UUID
from typing import TypedDict
from datetime import datetime


class ExpireUUID(TypedDict):
    uuid: UUID
    expires_at: datetime

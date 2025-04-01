from pydantic import BaseModel

from src.api.enums.DocumentType import DocumentType


class UserKYCRequest(BaseModel):
    bvn: str | None = None
    document_type: DocumentType | None = None
    document_id: str | None = None

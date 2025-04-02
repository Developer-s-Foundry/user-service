from typing import TypedDict, NotRequired


class KYCValidation(TypedDict):
    is_bvn_verified: NotRequired[bool]
    is_document_verified: NotRequired[bool]


class KYCSuccess(TypedDict):
    is_success: bool
    message: str

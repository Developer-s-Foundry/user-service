from typing import TypedDict


class AUTHMessages(TypedDict):
    pass


class USERMessages(TypedDict):
    pass


class PASSWORDRESETMessages(TypedDict):
    pass


class WITHDRAWALACCOUNTMessages(TypedDict):
    pass


class COMMONMessages(TypedDict):
    INTERNAL_SERVER_ERROR: str


class Messages(TypedDict):
    AUTH: AUTHMessages
    USER: USERMessages
    PASSWORD_RESET: PASSWORDRESETMessages
    WITHDRAWAL_ACCOUNT: WITHDRAWALACCOUNTMessages
    COMMON: COMMONMessages


MESSAGES: Messages = {
    "AUTH": {},
    "USER": {},
    "PASSWORD_RESET": {},
    "WITHDRAWAL_ACCOUNT": {},
    "COMMON": {"INTERNAL_SERVER_ERROR": "Something went wrong"},
}

__all__ = ["MESSAGES"]

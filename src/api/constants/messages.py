from typing import TypedDict


class COMMONMessages(TypedDict):
    INTERNAL_SERVER_ERROR: str


class Messages(TypedDict):
    COMMON: COMMONMessages


MESSAGES: Messages = {
    "COMMON": {"INTERNAL_SERVER_ERROR": "Something went wrong"},
}

__all__ = ["MESSAGES"]

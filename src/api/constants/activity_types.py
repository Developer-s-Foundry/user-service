from typing import TypedDict


class ActivityTypes(TypedDict):
    USER_REGISTRATION: str
    EMAIL_VALIDATION: str
    USER_LOGIN: str
    FETCH_USER: str
    UPDATE_USER: str
    SET_PIN: str
    ADD_WITHDRAW_ACCOUNT: str
    LIST_WITHDRAW_ACCOUNTS: str
    FETCH_WITHDRAW_ACCOUNT: str
    DELETE_WITHDRAW_ACCOUNT: str


ACTIVITY_TYPES: ActivityTypes = {
    "USER_REGISTRATION": "User registration",
    "EMAIL_VALIDATION": "Email validation",
    "USER_LOGIN": "User login",
    "FETCH_USER": "Get user details",
    "UPDATE_USER": "Update User Details",
    "SET_PIN": "Set user pin",
    "ADD_WITHDRAW_ACCOUNT": "Add withdraw account",
    "LIST_WITHDRAW_ACCOUNTS": "List withdraw accounts",
    "FETCH_WITHDRAW_ACCOUNT": "Get withdraw account",
    "DELETE_WITHDRAW_ACCOUNT": "Delete withdraw account",
}

__all__ = ["ACTIVITY_TYPES"]

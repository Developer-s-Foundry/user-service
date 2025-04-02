from typing import TypedDict


class ActivityTypes(TypedDict):
    EXCEPTION: str
    USER_REGISTRATION: str
    SEND_OTP: str
    VALIDATE_OTP: str
    RESEND_EMAIL: str
    EMAIL_VALIDATION: str
    USER_LOGIN: str
    FETCH_USER: str
    UPDATE_USER: str
    SET_PIN: str
    ADD_WITHDRAW_ACCOUNT: str
    UPDATE_WITHDRAW_ACCOUNT: str
    LIST_WITHDRAW_ACCOUNTS: str
    FETCH_WITHDRAW_ACCOUNT: str
    DELETE_WITHDRAW_ACCOUNT: str
    CHANGE_PASSWORD: str
    RESET_PASSWORD: str
    FETCH_NOK: str
    UPDATE_NOK: str
    FETCH_KYC: str
    UPDATE_KYC: str


ACTIVITY_TYPES: ActivityTypes = {
    "EXCEPTION": "Exception handler",
    "USER_REGISTRATION": "User registration",
    "SEND_OTP": "Send OTP",
    "VALIDATE_OTP": "Validate OTP",
    "RESEND_EMAIL": "Resend email validation",
    "EMAIL_VALIDATION": "Email validation",
    "USER_LOGIN": "User login",
    "FETCH_USER": "Get user details",
    "UPDATE_USER": "Update User Details",
    "SET_PIN": "Set user pin",
    "ADD_WITHDRAW_ACCOUNT": "Add withdraw account",
    "UPDATE_WITHDRAW_ACCOUNT": "Update withdraw account",
    "LIST_WITHDRAW_ACCOUNTS": "List withdraw accounts",
    "FETCH_WITHDRAW_ACCOUNT": "Get withdraw account",
    "DELETE_WITHDRAW_ACCOUNT": "Delete withdraw account",
    "CHANGE_PASSWORD": "Change user password",
    "RESET_PASSWORD": "Reset user password",
    "FETCH_NOK": "Fetch Next Of Kin",
    "UPDATE_NOK": "Update Next Of Kin",
    "FETCH_KYC": "Fetch KYC Information",
    "UPDATE_KYC": "Update KYC Information",
}

__all__ = ["ACTIVITY_TYPES"]

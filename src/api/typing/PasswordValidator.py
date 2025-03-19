from typing import Annotated

from pydantic import AfterValidator


def is_strong_password(password: str) -> str:
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must contain at least one digit")
    if not any(char.isupper() for char in password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(char.islower() for char in password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not any(char in "!@#$%^&*()-+" for char in password):
        raise ValueError("Password must contain at least one special character")
    return password


IsStrongPassword = Annotated[str, AfterValidator(is_strong_password)]

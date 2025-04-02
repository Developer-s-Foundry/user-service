import jwt
from django.http import HttpRequest
from ninja.security import HttpBearer

from src.env import jwt_config
from src.utils.logger import Logger


class Authentication(HttpBearer):
    def __init__(self, logger: Logger) -> None:
        super().__init__()
        self.logger = logger

    def authenticate(self, request: HttpRequest, token: str) -> str:
        jwt_data = jwt.decode(
            token,
            jwt_config["secret"],
            algorithms=["HS256"],
            options={"verify_signature": False},
        )
        self.logger.debug(
            {
                "activity_type": "Authenticate User",
                "message": "Successfully authenticated user",
                "metadata": {
                    "email": jwt_data["email"],
                    "user_id": jwt_data["user_id"],
                },
            }
        )
        setattr(request, "auth_email", jwt_data["email"])
        setattr(request, "auth_id", jwt_data["user_id"])
        return token


def get_authentication() -> Authentication:
    return Authentication(Logger("Authentication"))


authentication = get_authentication()

from http import HTTPStatus
from typing import Annotated

import jwt
from django.http import HttpRequest
from ninja.errors import HttpError
from ninja.security import HttpBearer

from src.env import jwt_config
from src.utils.logger import Logger
from src.utils.svcs import Service


@Service()
class Authentication(HttpBearer):
    def __init__(self, logger: Annotated[Logger, "Authentication"]) -> None:
        super().__init__()
        self.logger = logger

    def authenticate(self, request: HttpRequest, token: str) -> str:
        jwt_data = jwt.decode(
            token,
            jwt_config["secret"],
            algorithms=["HS256"],
            options={"verify_signature": False},
        )

        email = jwt_data.get("email")
        user_id = jwt_data.get("user_id")
        if not email or not user_id:
            message = "Invalid authentication token"
            self.logger.error(
                {
                    "activity_type": "Authenticate User",
                    "message": message,
                    "metadata": {"token": token},
                }
            )
            raise HttpError(HTTPStatus.UNAUTHORIZED, message)

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

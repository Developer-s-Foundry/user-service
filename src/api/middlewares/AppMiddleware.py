from typing import Annotated

import jwt
from django.http import HttpRequest
from ninja.security import HttpBearer

from src.env import jwt_config
from src.utils.svcs import Service
from src.utils.logger import Logger


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

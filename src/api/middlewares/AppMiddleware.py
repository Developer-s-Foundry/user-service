from http import HTTPStatus
from typing import Annotated

import jwt
from django.http import HttpRequest, HttpResponse
from ninja.errors import AuthenticationError
from ninja.security import HttpBearer

from src.env import jwt_config
from src.api.routes import api
from src.utils.svcs import Service
from src.utils.logger import Logger


@Service()
class Authentication(HttpBearer):
    def __init__(self, logger: Annotated[Logger, "Authentication"]) -> None:
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


@api.exception_handler(jwt.exceptions.InvalidTokenError)
@api.exception_handler(AuthenticationError)
def on_invalid_token(request: HttpRequest, exc: Exception) -> HttpResponse:
    Logger().debug(
        {
            "activity_type": "Exception handler",
            "message": "Unauthorised access",
            "metadata": {"exception": exc.__class__, "msg": str(exc)},
        }
    )
    return api.create_response(
        request, {"detail": "Unauthorized Access"}, status=HTTPStatus.UNAUTHORIZED
    )

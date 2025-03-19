from http import HTTPStatus

import jwt
from django.http import HttpRequest, HttpResponse
from ninja.security import HttpBearer

from src.env import jwt_config
from src.api.routes import api


class Authentication(HttpBearer):
    async def authenticate(self, request: HttpRequest, token: str) -> str:
        jwt_data = jwt.decode(
            token,
            jwt_config["secret"],
            algorithms=["HS256"],
            options={"verify_signature": False},
        )
        setattr(request, "auth_email", jwt_data["email"])
        setattr(request, "auth_id", jwt_data["user_id"])
        return token


@api.exception_handler(jwt.exceptions.InvalidTokenError)
def on_invalid_token(request: HttpRequest, exc: Exception) -> HttpResponse:
    return api.create_response(
        request, {"detail": "Unauthorized Access"}, status=HTTPStatus.UNAUTHORIZED
    )

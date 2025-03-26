from http import HTTPStatus

import jwt
from django.http import HttpRequest, HttpResponse
from ninja.errors import AuthenticationError

from src.api.routes import api
from src.utils.logger import Logger

exception_logger = Logger("API Exception")


@api.exception_handler(jwt.exceptions.InvalidTokenError)
@api.exception_handler(AuthenticationError)
def on_invalid_token(request: HttpRequest, exc: Exception) -> HttpResponse:
    exception_logger.debug(
        {
            "activity_type": "Exception handler",
            "message": "Unauthorised access",
            "metadata": {"exception": exc.__class__, "msg": str(exc)},
        }
    )
    return api.create_response(
        request, {"message": "Unauthorized Access"}, status=HTTPStatus.UNAUTHORIZED
    )

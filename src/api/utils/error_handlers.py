from http import HTTPStatus

import jwt
from django.http import HttpRequest, HttpResponse
from ninja.errors import AuthenticationError

from src.api.routes import api
from src.utils.logger import Logger
from src.api.constants.messages import MESSAGES
from src.api.constants.activity_types import ACTIVITY_TYPES

exception_logger = Logger("API Exception")


@api.exception_handler(jwt.exceptions.InvalidTokenError)
@api.exception_handler(AuthenticationError)
def on_invalid_token(request: HttpRequest, exc: Exception) -> HttpResponse:
    exception_logger.debug(
        {
            "activity_type": ACTIVITY_TYPES["EXCEPTION"],
            "message": MESSAGES["AUTH"]["UNAUTHORIZED"],
            "metadata": {"exception": exc.__class__},
        }
    )
    return api.create_response(
        request,
        {"message": MESSAGES["AUTH"]["UNAUTHORIZED"]},
        status=HTTPStatus.UNAUTHORIZED,
    )


@api.exception_handler(Exception)
def on_server_error(request: HttpRequest, exc: Exception) -> HttpResponse:
    exception_logger.error(
        {
            "activity_type": ACTIVITY_TYPES["EXCEPTION"],
            "message": str(exc),
            "metadata": {"exception": exc.__class__},
        }
    )
    return api.create_response(
        request,
        {"message": MESSAGES["COMMON"]["INTERNAL_SERVER_ERROR"]},
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

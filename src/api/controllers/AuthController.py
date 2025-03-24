from http import HTTPStatus
from typing import Annotated

from ninja.errors import HttpError

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.models.postgres import User
from src.api.services.AuthService import AuthService
from src.api.models.payload.requests.CreateUserRequest import CreateUserRequest
from src.api.models.payload.requests.AuthenticateUserOtp import AuthenticateUserOtp
from src.api.models.payload.requests.AuthenticateUserRequest import (
    AuthenticateUserRequest,
)


@Service()
class AuthController:
    def __init__(
        self, logger: Annotated[Logger, "AuthController"], auth_service: AuthService
    ) -> None:
        self.logger = logger
        self.auth_service = auth_service

    async def register(self, user_data: CreateUserRequest) -> User:
        try:
            user_exists = await self.auth_service.register(user_data)
            if user_exists["is_exists"]:
                raise HttpError(HTTPStatus.BAD_REQUEST, user_exists["message"])
            return user_exists["user"]
        except Exception as exc:
            if isinstance(exc, HttpError):
                raise
            self.logger.error(
                {
                    "activity_type": "User Registration",
                    "message": str(exc),
                    "metadata": user_data.model_dump(),
                }
            )
            raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")

    async def validate_email(self, credentials: AuthenticateUserOtp) -> dict:
        try:
            is_valid = await self.auth_service.validate_email(credentials)
            if not is_valid:
                raise HttpError(
                    HTTPStatus.BAD_REQUEST, "User email verification failed"
                )
            return {"message": "User email verification successful"}
        except Exception as exc:
            if isinstance(exc, HttpError):
                raise
            self.logger.error(
                {
                    "activity_type": "Email Validation",
                    "message": str(exc),
                    "metadata": credentials.model_dump(),
                }
            )
            raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")

    async def login(self, credentials: AuthenticateUserRequest) -> dict:
        try:
            auth_user = await self.auth_service.login(credentials)
            if not auth_user["is_success"]:
                raise HttpError(HTTPStatus.BAD_REQUEST, auth_user["message"])
            return {"user": auth_user["user"], "token": auth_user["token"]}
        except Exception as exc:
            if isinstance(exc, HttpError):
                raise
            self.logger.error(
                {
                    "activity_type": "User Login",
                    "message": str(exc),
                    "metadata": credentials.model_dump(),
                }
            )
            raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")

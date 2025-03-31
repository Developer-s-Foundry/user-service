from http import HTTPStatus
from typing import Annotated

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.services.AuthService import AuthService
from src.api.utils.response_format import error_response, success_response
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

    async def register(self, user_data: CreateUserRequest) -> dict:
        user_exists = await self.auth_service.register(user_data)
        if user_exists["is_exists"]:
            return error_response(
                user_exists["message"], status_code=HTTPStatus.BAD_REQUEST
            )
        return success_response(
            message=user_exists["message"],
            data=user_exists["user"],
            status_code=HTTPStatus.CREATED,
        )

    async def validate_email(self, credentials: AuthenticateUserOtp) -> dict:
        is_valid = await self.auth_service.validate_email(credentials)
        if not is_valid:
            return error_response(
                "User email verification failed", status_code=HTTPStatus.BAD_REQUEST
            )
        return success_response(
            message="User email verification successful", status_code=HTTPStatus.OK
        )

    async def login(self, credentials: AuthenticateUserRequest) -> dict:
        auth_user = await self.auth_service.login(credentials)
        if not auth_user["is_success"]:
            return error_response(
                message=auth_user["message"], status_code=HTTPStatus.BAD_REQUEST
            )
        return success_response(
            message="Successfully Logged in",
            data={"user": auth_user["user"], "token": auth_user["token"]},
            status_code=HTTPStatus.OK,
        )

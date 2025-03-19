from http import HTTPStatus

from ninja.errors import HttpError

from src.utils.svcs import Service
from src.api.models.postgres import User
from src.api.services.AuthService import AuthService
from src.api.models.payload.requests.CreateUserRequest import CreateUserRequest
from src.api.models.payload.requests.AuthenticateUserOtp import AuthenticateUserOtp
from src.api.models.payload.requests.AuthenticateUserRequest import (
    AuthenticateUserRequest,
)


@Service()
class AuthController:
    def __init__(self, auth_service: AuthService) -> None:
        self.auth_service = auth_service

    async def register(self, user_data: CreateUserRequest) -> User:
        user_exists = await self.auth_service.register(user_data)
        if user_exists["is_exists"]:
            raise HttpError(HTTPStatus.BAD_REQUEST, "User already exists")
        return user_exists["user"]

    async def validate_email(self, credentials: AuthenticateUserOtp) -> dict:
        is_valid = await self.auth_service.validate_email(credentials)
        if not is_valid:
            raise HttpError(HTTPStatus.BAD_REQUEST, "User email verification failed")
        return {"message": "User email verification successful"}

    async def login(self, credentials: AuthenticateUserRequest) -> dict:
        auth_user = await self.auth_service.login(credentials)
        if not auth_user["is_success"]:
            raise HttpError(HTTPStatus.BAD_REQUEST, auth_user["message"])
        return {"user": auth_user["user"], "token": auth_user["token"]}

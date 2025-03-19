from ninja import Router
from django.http import HttpRequest

from src.utils.svcs import Depends
from src.api.models.postgres import User as UserModel
from src.api.controllers.AuthController import AuthController
from src.api.models.payload.responses.User import UserResponse, UserLoginResponse
from src.api.models.payload.responses.MessageResponse import MessageResponse
from src.api.models.payload.requests.CreateUserRequest import CreateUserRequest
from src.api.models.payload.requests.AuthenticateUserOtp import AuthenticateUserOtp
from src.api.models.payload.requests.AuthenticateUserRequest import (
    AuthenticateUserRequest,
)

router = Router()


@router.post("/register", response=UserResponse)
async def create_user(request: HttpRequest, user_data: CreateUserRequest) -> UserModel:
    auth_controller = await Depends(AuthController)
    return await auth_controller.register(user_data)


@router.put("/email/verification", response=MessageResponse)
async def validate_email(
    request: HttpRequest, credentials: AuthenticateUserOtp
) -> dict:
    auth_controller = await Depends(AuthController)
    return await auth_controller.validate_email(credentials)


@router.post("/login", response=UserLoginResponse)
async def login(request: HttpRequest, credentials: AuthenticateUserRequest) -> dict:
    auth_controller = await Depends(AuthController)
    return await auth_controller.login(credentials)

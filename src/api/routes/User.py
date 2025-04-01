from http import HTTPStatus

from django.http import HttpRequest
from ninja import Router

from src.api.controllers.UserController import UserController
from src.api.models.payload.requests.Pin import Pin
from src.api.models.payload.requests.UpdateUserRequest import (
    ChangeUserPasswordRequest, UpdateUserRequest)
from src.api.models.payload.responses.ErrorResponse import (
    ErrorResponse, ServerErrorResponse)
from src.api.models.payload.responses.SuccessResponse import SuccessResponse
from src.api.models.payload.responses.User import UserResponse
from src.utils.svcs import ADepends

router = Router()


@router.put(
    "/pins",
    response={
        HTTPStatus.OK: SuccessResponse,
        HTTPStatus.BAD_REQUEST: ErrorResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR: ServerErrorResponse,
    },
)
async def set_account_pin(request: HttpRequest, user_pin: Pin) -> tuple:
    user_id = getattr(request, "auth_id", "")
    user_controller = await ADepends(UserController)
    return await user_controller.set_account_pin(user_id, user_pin)


@router.get(
    "/",
    response={
        HTTPStatus.OK: SuccessResponse[UserResponse],
        HTTPStatus.BAD_REQUEST: ErrorResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR: ServerErrorResponse,
    },
)
async def get_user(request: HttpRequest) -> tuple:
    user_id = getattr(request, "auth_id", "")
    user_controller = await ADepends(UserController)
    return await user_controller.get_user(user_id)


@router.put(
    "/",
    response={
        HTTPStatus.OK: SuccessResponse[UserResponse],
        HTTPStatus.BAD_REQUEST: ErrorResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR: ServerErrorResponse,
    },
)
async def update_user(request: HttpRequest, user_data: UpdateUserRequest) -> tuple:
    user_id = getattr(request, "auth_id", "")
    user_controller = await ADepends(UserController)
    return await user_controller.update_user(user_id, user_data)


@router.put(
    "/change-password",
    response={
        HTTPStatus.OK: SuccessResponse,
        HTTPStatus.BAD_REQUEST: ErrorResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR: ServerErrorResponse,
    },
)
async def update_password(request: HttpRequest, user_data: ChangeUserPasswordRequest) -> tuple:
    user_id = getattr(request, "auth_id", "")
    ('User ID:', user_id)
    user_controller = await ADepends(UserController)
    return await user_controller.change_password(user_id, user_data)
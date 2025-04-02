from http import HTTPStatus

from django.http import HttpRequest
from ninja import Router

from src.api.controllers.PasswordResetController import PasswordResetController
from src.api.models.payload.requests.PasswordResetRequest import (
    ConfirmPasswordResetRequest, PasswordResetRequest)
from src.api.models.payload.responses.ErrorResponse import (
    ErrorResponse, ServerErrorResponse)
from src.api.models.payload.responses.SuccessResponse import SuccessResponse
from src.utils.svcs import ADepends

router = Router()


@router.post("/", response={
    HTTPStatus.OK: SuccessResponse,
    HTTPStatus.BAD_REQUEST: ErrorResponse,
    HTTPStatus.INTERNAL_SERVER_ERROR: ServerErrorResponse,

})
async def reset_password(
    request: HttpRequest, credentials: PasswordResetRequest
) -> tuple:
    reset_controller = await ADepends(PasswordResetController)
    return await reset_controller.request_password_reset(credentials)



# TODO: Implement router for password reset confirm and change password

@router.post("/confirm", response={
    HTTPStatus.OK: SuccessResponse,
    HTTPStatus.BAD_REQUEST: ErrorResponse,
    HTTPStatus.INTERNAL_SERVER_ERROR: ServerErrorResponse,
})
async def confirm_password_reset(
    request: HttpRequest, credentials: ConfirmPasswordResetRequest
) -> tuple:
    reset_controller = await ADepends(PasswordResetController)
    return await reset_controller.confirm_password_reset(credentials)

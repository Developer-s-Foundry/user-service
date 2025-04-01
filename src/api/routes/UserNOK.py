from http import HTTPStatus

from ninja import Router
from django.http import HttpRequest

from src.utils.svcs import ADepends
from src.api.controllers.UserNOKController import UserNOKController
from src.api.models.payload.responses.UserNOK import UserNOKResponse
from src.api.models.payload.requests.UserNOKRequest import UserNOKRequest
from src.api.models.payload.responses.ErrorResponse import (
    ErrorResponse,
    ServerErrorResponse,
)
from src.api.models.payload.responses.SuccessResponse import SuccessResponse

router = Router()


@router.get(
    "/",
    response={
        HTTPStatus.OK: SuccessResponse[UserNOKResponse],
        HTTPStatus.BAD_REQUEST: ErrorResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR: ServerErrorResponse,
    },
)
async def get_next_of_kin(request: HttpRequest) -> tuple:
    user_id = getattr(request, "auth_id", "")
    nok_controller = await ADepends(UserNOKController)
    return await nok_controller.get_user_nok(user_id)


@router.put(
    "/",
    response={
        HTTPStatus.OK: SuccessResponse,
        HTTPStatus.BAD_REQUEST: ErrorResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR: ServerErrorResponse,
    },
)
async def update_next_of_kin(request: HttpRequest, user_data: UserNOKRequest) -> tuple:
    user_id = getattr(request, "auth_id", "")
    nok_controller = await ADepends(UserNOKController)
    return await nok_controller.update_user_nok(user_id, user_data)

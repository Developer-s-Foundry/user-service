from http import HTTPStatus

from ninja import Router
from django.http import HttpRequest

from src.utils.svcs import ADepends
from src.api.controllers.UserKYCController import UserKYCController
from src.api.models.payload.responses.UserKYC import UserKYCResponse
from src.api.models.payload.requests.UserKYCRequest import UserKYCRequest
from src.api.models.payload.responses.ErrorResponse import (
    ErrorResponse,
    ServerErrorResponse,
)
from src.api.models.payload.responses.SuccessResponse import SuccessResponse

router = Router()


@router.get(
    "/",
    response={
        HTTPStatus.OK: SuccessResponse[UserKYCResponse],
        HTTPStatus.BAD_REQUEST: ErrorResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR: ServerErrorResponse,
    },
)
async def get_kyc_information(request: HttpRequest) -> tuple:
    user_id = getattr(request, "auth_id", "")
    kyc_controller = await ADepends(UserKYCController)
    return await kyc_controller.get_user_kyc(user_id)


@router.put(
    "/",
    response={
        HTTPStatus.OK: SuccessResponse,
        HTTPStatus.BAD_REQUEST: ErrorResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR: ServerErrorResponse,
    },
)
async def update_kyc_information(
    request: HttpRequest, user_data: UserKYCRequest
) -> tuple:
    user_id = getattr(request, "auth_id", "")
    kyc_controller = await ADepends(UserKYCController)
    return await kyc_controller.update_user_kyc(user_id, user_data)

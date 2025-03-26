from http import HTTPStatus

from ninja import Router
from django.http import HttpRequest

from src.utils.svcs import ADepends
from src.api.models.payload.responses.ErrorResponse import (
    ErrorResponse,
    ServerErrorResponse,
)
from src.api.controllers.WithdrawalAccountController import WithdrawalAccountController
from src.api.models.payload.responses.SuccessResponse import SuccessResponse
from src.api.models.payload.responses.UserWithdrawalInformation import (
    UserWithdrawalInformation as UserWithdrawalInformationResponse,
)
from src.api.models.payload.requests.AddWithdrawalAccountRequest import (
    AddWithdrawalAccountRequest,
)

router = Router()


@router.post(
    "/",
    response={
        HTTPStatus.CREATED: SuccessResponse,
        HTTPStatus.BAD_REQUEST: ErrorResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR: ServerErrorResponse,
    },
)
async def add_withdrawal_account(
    request: HttpRequest, account_data: AddWithdrawalAccountRequest
) -> dict:
    user_id = getattr(request, "auth_id", "")
    withdraw_controller = await ADepends(WithdrawalAccountController)
    return await withdraw_controller.add_withdrawal_account(user_id, account_data)


@router.get(
    "/",
    response={
        HTTPStatus.OK: SuccessResponse[list[UserWithdrawalInformationResponse]],
        HTTPStatus.INTERNAL_SERVER_ERROR: ServerErrorResponse,
    },
)
async def list_withdrawal_accounts(
    request: HttpRequest,
) -> dict:
    user_id = getattr(request, "auth_id", "")
    withdraw_controller = await ADepends(WithdrawalAccountController)
    return await withdraw_controller.list_withdrawal_accounts(user_id)


@router.get(
    "/{int:id}",
    response={
        HTTPStatus.OK: SuccessResponse[UserWithdrawalInformationResponse],
        HTTPStatus.NOT_FOUND: ErrorResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR: ServerErrorResponse,
    },
)
async def get_withdrawal_account(request: HttpRequest, id: int) -> dict:
    user_id = getattr(request, "auth_id", "")
    withdraw_controller = await ADepends(WithdrawalAccountController)
    return await withdraw_controller.get_withdrawal_account(user_id, id)


@router.delete(
    "/{int:id}",
    response={
        HTTPStatus.OK: SuccessResponse,
        HTTPStatus.FORBIDDEN: ErrorResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR: ServerErrorResponse,
    },
)
async def delete_withdrawal_account(request: HttpRequest, id: int) -> dict:
    user_id = getattr(request, "auth_id", "")
    withdraw_controller = await ADepends(WithdrawalAccountController)
    return await withdraw_controller.delete_withdrawal_account(user_id, id)

from ninja import Router
from django.http import HttpRequest

from src.utils.svcs import ADepends
from src.api.models.postgres import (
    UserWithdrawalInformation as UserWithdrawalInformationModel,
)
from src.api.controllers.WithdrawalAccountController import WithdrawalAccountController
from src.api.models.payload.responses.MessageResponse import MessageResponse
from src.api.models.payload.responses.UserWithdrawalInformation import (
    UserWithdrawalInformation as UserWithdrawalInformationResponse,
)
from src.api.models.payload.requests.AddWithdrawalAccountRequest import (
    AddWithdrawalAccountRequest,
)

router = Router()


@router.post("/", response={201: MessageResponse})
async def add_withdrawal_account(
    request: HttpRequest, account_data: AddWithdrawalAccountRequest
) -> tuple:
    user_id = getattr(request, "auth_id", "")
    withdraw_controller = await ADepends(WithdrawalAccountController)
    return await withdraw_controller.add_withdrawal_account(user_id, account_data)


@router.get("/", response=list[UserWithdrawalInformationResponse])
async def list_withdrawal_accounts(
    request: HttpRequest,
) -> list[UserWithdrawalInformationModel]:
    user_id = getattr(request, "auth_id", "")
    withdraw_controller = await ADepends(WithdrawalAccountController)
    return await withdraw_controller.list_withdrawal_accounts(user_id)


@router.get("/{int:id}", response=UserWithdrawalInformationResponse)
async def get_withdrawal_account(
    request: HttpRequest, id: int
) -> UserWithdrawalInformationModel:
    user_id = getattr(request, "auth_id", "")
    withdraw_controller = await ADepends(WithdrawalAccountController)
    return await withdraw_controller.get_withdrawal_account(user_id, id)


@router.delete("/{int:id}", response=MessageResponse)
async def delete_withdrawal_account(request: HttpRequest, id: int) -> dict:
    user_id = getattr(request, "auth_id", "")
    withdraw_controller = await ADepends(WithdrawalAccountController)
    return await withdraw_controller.delete_withdrawal_account(user_id, id)

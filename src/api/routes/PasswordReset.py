from ninja import Router
from django.http import HttpRequest

from src.utils.svcs import ADepends
from src.api.controllers.PasswordResetController import PasswordResetController
from src.api.models.payload.responses.SuccessResponse import SuccessResponse
from src.api.models.payload.requests.PasswordResetRequest import PasswordResetRequest

router = Router()


@router.post("/", response=SuccessResponse)
async def reset_password(
    request: HttpRequest, credentials: PasswordResetRequest
) -> dict:
    reset_controller = await ADepends(PasswordResetController)
    return await reset_controller.request_password_reset(credentials)

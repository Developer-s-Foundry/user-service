from ninja import Router
from django.http import HttpRequest

from src.utils.svcs import Depends
from src.api.models.postgres import User as UserModel
from src.api.controllers.UserController import UserController
from src.api.models.payload.requests.Pin import Pin
from src.api.models.payload.responses.User import UserResponse
from src.api.models.payload.responses.MessageResponse import MessageResponse
from src.api.models.payload.requests.UpdateUserRequest import UpdateUserRequest

router = Router()


@router.put("/pins", response=MessageResponse)
async def set_account_pin(request: HttpRequest, user_pin: Pin) -> dict:
    user_id = getattr(request, "auth_id", "")
    user_controller = await Depends(UserController)
    return await user_controller.set_account_pin(user_id, user_pin)


@router.get("/", response=UserResponse)
async def get_user(request: HttpRequest) -> UserModel:
    user_id = getattr(request, "auth_id", "")
    user_controller = await Depends(UserController)
    return await user_controller.get_user(user_id)


@router.put("/", response=UserResponse)
async def update_user(request: HttpRequest, user_data: UpdateUserRequest) -> UserModel:
    user_id = getattr(request, "auth_id", "")
    user_controller = await Depends(UserController)
    return await user_controller.update_user(user_id, user_data)

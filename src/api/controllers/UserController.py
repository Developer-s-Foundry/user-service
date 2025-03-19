from http import HTTPStatus

from ninja.errors import HttpError

from src.utils.svcs import Service
from src.api.models.postgres import User
from src.api.services.UserService import UserService
from src.api.models.payload.requests.Pin import Pin
from src.api.models.payload.requests.UpdateUserRequest import UpdateUserRequest


@Service()
class UserController:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    async def get_user(self, id: str) -> User:
        user = await self.user_service.get_user_information(id)
        if not user:
            raise HttpError(HTTPStatus.NOT_FOUND, "User does not exists")
        return user

    async def update_user(self, id: str, user_data: UpdateUserRequest) -> User:
        user_data._id = id
        updated_user = await self.user_service.update(user_data)
        if not updated_user["is_success"]:
            raise HttpError(HTTPStatus.BAD_REQUEST, updated_user["message"])
        return updated_user["user"]

    async def set_account_pin(self, id: str, user_pin: Pin) -> dict:
        updated_pin = await self.user_service.set_pin(id, user_pin.pin)
        if not updated_pin["is_success"]:
            raise HttpError(400, updated_pin["message"])
        return {"message": updated_pin["message"]}

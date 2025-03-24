from http import HTTPStatus
from typing import Annotated

from ninja.errors import HttpError

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.models.postgres import User
from src.api.services.UserService import UserService
from src.api.models.payload.requests.Pin import Pin
from src.api.models.payload.requests.UpdateUserRequest import UpdateUserRequest


@Service()
class UserController:
    def __init__(
        self, logger: Annotated[Logger, "UserController"], user_service: UserService
    ) -> None:
        self.logger = logger
        self.user_service = user_service

    async def get_user(self, id: str) -> User:
        try:
            user = await self.user_service.get_user_information(id)
            if not user:
                raise HttpError(HTTPStatus.NOT_FOUND, "User does not exists")
            return user
        except Exception as exc:
            if isinstance(exc, HttpError):
                raise
            self.logger.error(
                {
                    "activity_type": "Get User Details",
                    "message": str(exc),
                    "metadata": {"user": {"id": id}},
                }
            )
            raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")

    async def update_user(self, id: str, user_data: UpdateUserRequest) -> User:
        try:
            user_data._id = id
            updated_user = await self.user_service.update(user_data)
            if not updated_user["is_success"]:
                raise HttpError(HTTPStatus.BAD_REQUEST, updated_user["message"])
            return updated_user["user"]
        except Exception as exc:
            if isinstance(exc, HttpError):
                raise
            self.logger.error(
                {
                    "activity_type": "Update User Details",
                    "message": str(exc),
                    "metadata": {
                        "user": {"id": id},
                        "new_data": user_data.model_dump(),
                    },
                }
            )
            raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")

    async def set_account_pin(self, id: str, user_pin: Pin) -> dict:
        try:
            updated_pin = await self.user_service.set_pin(id, user_pin.pin)
            if not updated_pin["is_success"]:
                raise HttpError(400, updated_pin["message"])
            return {"message": updated_pin["message"]}
        except Exception as exc:
            if isinstance(exc, HttpError):
                raise
            self.logger.error(
                {
                    "activity_type": "Set User Pin",
                    "message": str(exc),
                    "metadata": {"user": {"id": id, "pin": user_pin.pin}},
                }
            )
            raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")

from http import HTTPStatus
from typing import Annotated

from src.api.models.payload.requests.Pin import Pin
from src.api.models.payload.requests.UpdateUserRequest import (
    ChangeUserPasswordRequest, UpdateUserRequest)
from src.api.services.UserService import UserService
from src.api.utils.response_format import error_response, success_response
from src.utils.logger import Logger
from src.utils.svcs import Service


@Service()
class UserController:
    def __init__(
        self, logger: Annotated[Logger, "UserController"], user_service: UserService
    ) -> None:
        self.logger = logger
        self.user_service = user_service

    async def get_user(self, id: str) -> tuple:
        user = await self.user_service.get_user_information(id)
        if not user:
            return error_response(
                message="User does not exists", status_code=HTTPStatus.NOT_FOUND
            )
        return success_response(
            message="Successfully retrieved user detail",
            data=user,
            status_code=HTTPStatus.OK,
        )

    async def update_user(self, id: str, user_data: UpdateUserRequest) -> tuple:
        user_data._id = id
        updated_user = await self.user_service.update(user_data)
        if not updated_user["is_success"]:
            return error_response(
                message=updated_user["message"], status_code=HTTPStatus.BAD_REQUEST
            )
        return success_response(
            message=updated_user["message"],
            data=updated_user["user"],
            status_code=HTTPStatus.OK,
        )

    async def set_account_pin(self, id: str, user_pin: Pin) -> tuple:
        updated_pin = await self.user_service.set_pin(id, user_pin.pin)
        if not updated_pin["is_success"]:
            return error_response(
                message=updated_pin["message"], status_code=HTTPStatus.BAD_REQUEST
            )
        return success_response(
            message=updated_pin["message"], status_code=HTTPStatus.OK
        )

    async def change_password(self, id: str, user_data: ChangeUserPasswordRequest) -> tuple:
        user_data._id = id
        updated_password = await self.user_service.change_password(user_data)
        if not updated_password["is_success"]:
            return error_response(
                message=updated_password["message"], status_code=HTTPStatus.BAD_REQUEST
            )
        return success_response(
            message=updated_password["message"],
            status_code=HTTPStatus.OK,
        )
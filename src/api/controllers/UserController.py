from http import HTTPStatus
from typing import Annotated

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.constants.messages import MESSAGES
from src.api.services.UserService import UserService
from src.api.constants.activity_types import ACTIVITY_TYPES
from src.api.response.response_format import error_response, success_response
from src.api.models.payload.requests.Pin import Pin
from src.api.models.payload.requests.UpdateUserRequest import UpdateUserRequest


@Service()
class UserController:
    def __init__(
        self, logger: Annotated[Logger, "UserController"], user_service: UserService
    ) -> None:
        self.logger = logger
        self.user_service = user_service

    async def get_user(self, id: str) -> dict:
        try:
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
        except Exception as exc:
            self.logger.error(
                {
                    "activity_type": ACTIVITY_TYPES["FETCH_USER"],
                    "message": str(exc),
                    "metadata": {"user": {"id": id}},
                }
            )
            return error_response(
                message=MESSAGES["COMMON"]["INTERNAL_SERVER_ERROR"],
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    async def update_user(self, id: str, user_data: UpdateUserRequest) -> dict:
        try:
            user_data._id = id
            updated_user = await self.user_service.update(user_data)
            if not updated_user["is_success"]:
                return error_response(
                    message=updated_user["message"],
                    status_code=HTTPStatus.BAD_REQUEST,
                )
            return success_response(
                message=updated_user["message"],
                data=updated_user["user"],
                status_code=HTTPStatus.OK,
            )
        except Exception as exc:
            self.logger.error(
                {
                    "activity_type": ACTIVITY_TYPES["UPDATE_USER"],
                    "message": str(exc),
                    "metadata": {
                        "user": {"id": id},
                        "new_data": user_data.model_dump(),
                    },
                }
            )
            return error_response(
                message=MESSAGES["COMMON"]["INTERNAL_SERVER_ERROR"],
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    async def set_account_pin(self, id: str, user_pin: Pin) -> dict:
        try:
            updated_pin = await self.user_service.set_pin(id, user_pin.pin)
            if not updated_pin["is_success"]:
                return error_response(
                    message=updated_pin["message"], status_code=HTTPStatus.BAD_REQUEST
                )
            return success_response(
                message=updated_pin["message"], status_code=HTTPStatus.OK
            )
        except Exception as exc:
            self.logger.error(
                {
                    "activity_type": ACTIVITY_TYPES["SET_PIN"],
                    "message": str(exc),
                    "metadata": {"user": {"id": id, "pin": user_pin.pin}},
                }
            )
            return error_response(
                message=MESSAGES["COMMON"]["INTERNAL_SERVER_ERROR"],
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

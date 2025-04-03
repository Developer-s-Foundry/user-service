from typing import Annotated

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.models.postgres import User
from src.api.constants.messages import MESSAGES, DYNAMIC_MESSAGES
from src.api.typing.UserSuccess import UserSuccess
from src.api.constants.activity_types import ACTIVITY_TYPES
from src.api.repositories.UserRepository import UserRepository
from src.api.models.payload.requests.UpdateUserRequest import (
    UpdateUserRequest,
    ChangeUserPasswordRequest,
)

from .UtilityService import UtilityService


@Service()
class UserService:
    def __init__(
        self,
        logger: Annotated[Logger, "UserService"],
        utility_service: UtilityService,
    ) -> None:
        self.logger = logger
        self.utility_service = utility_service

    async def get_user_information(self, id: str) -> User:
        existing_user = await UserRepository.find_by_id(id)
        user = self.utility_service.sanitize_user_object(existing_user)
        if user:
            self.logger.info(
                {
                    "activity_type": ACTIVITY_TYPES["FETCH_USER"],
                    "message": DYNAMIC_MESSAGES["COMMON"]["FETCHED_SUCCESS"]("User"),
                    "metadata": {"user": {"id": user.id, "email": user.email}},
                }
            )
        else:
            self.logger.warn(
                {
                    "activity_type": ACTIVITY_TYPES["FETCH_USER"],
                    "message": DYNAMIC_MESSAGES["COMMON"]["FETCHED_FAILED"]("User"),
                    "metadata": {"user": {"id": id}},
                }
            )
        return user

    async def set_pin(self, id: str, pin: str) -> UserSuccess:
        existing_user = await UserRepository.find_by_id(id)
        if not existing_user:
            self.logger.warn(
                {
                    "activity_type": ACTIVITY_TYPES["SET_PIN"],
                    "message": MESSAGES["USER"]["DOESNT_EXIST"],
                    "metadata": {"user": {"id": id}},
                }
            )
            return {"is_success": False, "message": MESSAGES["USER"]["DOESNT_EXIST"]}
        if existing_user.pin:
            self.logger.info(
                {
                    "activity_type": ACTIVITY_TYPES["SET_PIN"],
                    "message": MESSAGES["USER"]["PIN_EXISTS"],
                    "metadata": {
                        "user": {"id": existing_user.id, "email": existing_user.email}
                    },
                }
            )
            return {
                "is_success": False,
                "message": MESSAGES["USER"]["PIN_EXISTS"],
            }
        await UserRepository.update_by_user(existing_user, {"pin": pin})
        self.logger.info(
            {
                "activity_type": ACTIVITY_TYPES["SET_PIN"],
                "message": MESSAGES["USER"]["PIN_SET"],
                "metadata": {
                    "user": {"id": existing_user.id, "email": existing_user.email}
                },
            }
        )
        return {
            "is_success": True,
            "message": MESSAGES["USER"]["PIN_SET"],
        }

    async def update(self, id: str, req: UpdateUserRequest) -> UserSuccess:
        existing_user = await UserRepository.find_by_id(id)
        if not existing_user:
            self.logger.warn(
                {
                    "activity_type": ACTIVITY_TYPES["UPDATE_USER"],
                    "message": DYNAMIC_MESSAGES["COMMON"]["FETCHED_FAILED"]("User"),
                    "metadata": {"user": {"id": id}},
                }
            )
            return {"is_success": False, "message": MESSAGES["USER"]["DOESNT_EXIST"]}

        updated_user = await UserRepository.update_by_id(
            id, req.model_dump(exclude_unset=True)
        )

        self.logger.info(
            {
                "activity_type": ACTIVITY_TYPES["UPDATE_USER"],
                "message": MESSAGES["USER"]["UPDATED"],
                "metadata": {
                    "user": {"id": id},
                    "new_data": req.model_dump(exclude_unset=True),
                },
            }
        )
        user = self.utility_service.sanitize_user_object(updated_user)

        return {"is_success": True, "user": user}

    async def change_password(
        self, id: str, req: ChangeUserPasswordRequest
    ) -> UserSuccess:
        existing_user = await UserRepository.find_by_id(id)
        old_password = req.old_password
        new_password = req.new_password

        if not existing_user:
            self.logger.warn(
                {
                    "activity_type": ACTIVITY_TYPES["CHANGE_PASSWORD"],
                    "message": DYNAMIC_MESSAGES["COMMON"]["FETCHED_FAILED"]("User"),
                    "metadata": {"user": {"id": id}},
                }
            )
            return {"is_success": False, "message": MESSAGES["USER"]["DOESNT_EXIST"]}

        is_valid_old_password = await self.utility_service.compare_hash(
            old_password, existing_user.password
        )
        if not is_valid_old_password:
            message = MESSAGES["USER"]["INCORRECT_PASSWORD"]
            self.logger.warn(
                {
                    "activity_type": ACTIVITY_TYPES["CHANGE_PASSWORD"],
                    "message": message,
                    "metadata": {"user": {"id": id}},
                }
            )
            return {"is_success": False, "message": message}

        new_password_hash = await self.utility_service.hash_string(new_password)
        await UserRepository.update_by_user(
            existing_user, {"password": new_password_hash}
        )
        message = MESSAGES["USER"]["PASSWORD_CHANGED"]
        self.logger.info(
            {
                "activity_type": ACTIVITY_TYPES["CHANGE_PASSWORD"],
                "message": message,
                "metadata": {"user": {"id": id}},
            }
        )

        return {"is_success": True, "message": message}

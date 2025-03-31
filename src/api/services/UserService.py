from typing import Annotated

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.models.postgres import User
from src.api.typing.UserSuccess import UserSuccess
from src.api.constants.activity_types import ACTIVITY_TYPES
from src.api.repositories.UserRepository import UserRepository
from src.api.models.payload.requests.UpdateUserRequest import UpdateUserRequest

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
                    "message": "User fetched succesfully",
                    "metadata": {"user": {"id": user.id, "email": user.email}},
                }
            )
        else:
            self.logger.warn(
                {
                    "activity_type": "Get User Details",
                    "message": "User fetch failed",
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
                    "message": "User does not exist",
                    "metadata": {"user": {"id": id}},
                }
            )
            return {"is_success": False, "message": "User doesn't exist!"}
        if existing_user.pin:
            self.logger.info(
                {
                    "activity_type": ACTIVITY_TYPES["SET_PIN"],
                    "message": "User already has a pin",
                    "metadata": {
                        "user": {"id": existing_user.id, "email": existing_user.email}
                    },
                }
            )
            return {
                "is_success": False,
                "message": "You already have a transaction PIN on your account!",
            }
        await UserRepository.update_by_user(existing_user, {"pin": pin})
        self.logger.info(
            {
                "activity_type": ACTIVITY_TYPES["SET_PIN"],
                "message": "User PIN set successfully",
                "metadata": {
                    "user": {"id": existing_user.id, "email": existing_user.email}
                },
            }
        )
        return {"is_success": True, "message": "Transaction PIN created!"}

    async def update(self, req: UpdateUserRequest) -> UserSuccess:
        id = req._id

        existing_user = await UserRepository.find_by_id(id)
        if not existing_user:
            self.logger.warn(
                {
                    "activity_type": ACTIVITY_TYPES["UPDATE_USER"],
                    "message": "User fetch failed",
                    "metadata": {"user": {"id": id}},
                }
            )
            return {"is_success": False, "message": "User doesn't exist!"}

        updated_user = await UserRepository.update_by_id(
            id, req.model_dump(exclude_unset=True)
        )

        self.logger.info(
            {
                "activity_type": ACTIVITY_TYPES["UPDATE_USER"],
                "message": "User updated successfully",
                "metadata": {
                    "user": {"id": id},
                    "new_data": req.model_dump(exclude_unset=True),
                },
            }
        )
        user = self.utility_service.sanitize_user_object(updated_user)

        return {"is_success": True, "user": user}

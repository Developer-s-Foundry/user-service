from typing import Annotated

from faststream.rabbit import RabbitRouter

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.models.postgres import User
from src.api.constants.messages import MESSAGES, DYNAMIC_MESSAGES
from src.api.typing.UserSuccess import UserSuccess
from src.api.constants.activity_types import ACTIVITY_TYPES
from src.api.repositories.UserRepository import UserRepository
from src.api.models.payload.requests.CreateUserRequest import CreateUserRequest
from src.api.models.payload.requests.UpdateUserRequest import UpdateUserRequest

from .UtilityService import UtilityService

UserRouter = RabbitRouter()


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


    @staticmethod
    @UserRouter.subscriber("create-user")
    async def register(message: dict) -> None:
        logger = Logger('UserService')
        user_data = CreateUserRequest(
            id=message["id"],
            email=message["email"],
            first_name='',
            last_name='',
            address='',
            phone_number='',
            profile_picture='',
            pin='',
        )
        new_user = await UserRepository.add(user_data)

        logger.info(
            {
                "activity_type": ACTIVITY_TYPES["USER_REGISTRATION"],
                "message": MESSAGES["REGISTRATION"]["USER_REGISTERED"],
                "metadata": {
                    "user": {"id": new_user.id, "email": new_user.email}
                },
            }
        )

    @staticmethod
    @UserRouter.subscriber("validate-user")
    async def validate_user(message: dict) -> None:
        logger = Logger('UserService')
        user = await UserRepository.find_by_id(message["id"])

        if not user:
            logger.warn(
                {
                    "activity_type": ACTIVITY_TYPES["EMAIL_VALIDATION"],
                    "message": DYNAMIC_MESSAGES["COMMON"]["FETCHED_FAILED"]("User"),
                    "metadata": {"user": {"id": message["id"]}},
                }
            )
            return 
        
        await UserRepository.update_by_user(
            user, {"is_active": True, "is_enabled": True, "is_validated": True}
        )

        logger.info(
            {
                "activity_type": ACTIVITY_TYPES["EMAIL_VALIDATION"],
                "message": MESSAGES["REGISTRATION"]["VERIFICATION_SUCCESS"],
                "metadata": {
                    "user": {"id": user.id, "email": user.email}
                },
            }
        )

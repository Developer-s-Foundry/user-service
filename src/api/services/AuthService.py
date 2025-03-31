from typing import Annotated

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.typing.UserExists import UserExists
from src.api.constants.messages import MESSAGES
from src.api.typing.UserSuccess import UserSuccess
from src.api.constants.activity_types import ACTIVITY_TYPES
from src.api.repositories.UserRepository import UserRepository
from src.api.models.payload.requests.CreateUserRequest import CreateUserRequest
from src.api.models.payload.requests.AuthenticateUserOtp import AuthenticateUserOtp
from src.api.models.payload.requests.AuthenticateUserRequest import (
    AuthenticateUserRequest,
)

from .UtilityService import UtilityService


@Service()
class AuthService:
    def __init__(
        self, logger: Annotated[Logger, "AuthService"], utility_service: UtilityService
    ) -> None:
        self.logger = logger
        self.utility_service = utility_service

    async def register(self, req: CreateUserRequest) -> UserExists:
        email = req.email
        password = req.password

        existing_user = await UserRepository.find_by_email(email)
        if existing_user:
            message = MESSAGES["REGISTRATION"]["EMAIL_EXISTS"]
            self.logger.info(
                {
                    "activity_type": ACTIVITY_TYPES["USER_REGISTRATION"],
                    "message": message,
                    "metadata": {"user": {"email": existing_user.email}},
                }
            )
            return {
                "is_exists": True,
                "user": existing_user,
                "message": message,
            }

        hashed_password: str = await self.utility_service.hash_string(password)
        req = req.model_copy(update={"password": hashed_password})

        created_user = await UserRepository.add(req)
        otp = self.utility_service.generate_random_string(length=6, numeric_only=True)

        otp  # Send OTP to user

        user = self.utility_service.sanitize_user_object(created_user)

        message = MESSAGES["REGISTRATION"]["USER_REGISTERED"]
        self.logger.info(
            {
                "activity_type": ACTIVITY_TYPES["USER_REGISTRATION"],
                "message": message,
                "metadata": {"user": {"email": user.email}},
            }
        )
        return {
            "is_exists": False,
            "user": user,
            "message": message,
        }

    async def validate_email(self, req: AuthenticateUserOtp) -> bool:
        email = req.email
        otp = req.otp

        user = await UserRepository.find_by_email(email)
        if not user:
            self.logger.error(
                {
                    "activity_type": ACTIVITY_TYPES["EMAIL_VALIDATION"],
                    "message": MESSAGES["USER"]["DOESNT_EXIST"],
                    "metadata": {"email": email, "otp": otp},
                }
            )
            return False

        # check otp storage to validate sent otp
        email
        otp

        await UserRepository.update_by_user(
            user, {"is_active": True, "is_enabled": True, "is_validated": True}
        )

        return True

    async def login(self, req: AuthenticateUserRequest) -> UserSuccess:
        email = req.email
        password = req.password

        existing_user = await UserRepository.find_by_email(email)
        if not existing_user:
            message = MESSAGES["AUTH"]["INVALID_CRED"]
            self.logger.info(
                {
                    "activity_type": ACTIVITY_TYPES["USER_LOGIN"],
                    "message": message,
                    "metadata": req.model_dump(),
                }
            )
            return {"is_success": False, "message": message}

        is_password_check_ok = await self.utility_service.compare_hash(
            password, existing_user.password
        )
        if not is_password_check_ok:
            message = MESSAGES["AUTH"]["INVALID_CRED"]
            self.logger.info(
                {
                    "activity_type": ACTIVITY_TYPES["USER_LOGIN"],
                    "message": message,
                    "metadata": req.model_dump(),
                }
            )
            return {"is_success": False, "message": message}

        if not existing_user.is_validated:
            # resend otp
            message = MESSAGES["AUTH"]["NOT_VALIDATED"]
            self.logger.info(
                {
                    "activity_type": ACTIVITY_TYPES["USER_LOGIN"],
                    "message": message,
                    "metadata": req.model_dump(),
                }
            )
            return {
                "is_success": False,
                "message": message,
            }

        if not existing_user.is_active:
            message = MESSAGES["AUTH"]["NOT_ACTIVE"]
            self.logger.info(
                {
                    "activity_type": ACTIVITY_TYPES["USER_LOGIN"],
                    "message": message,
                    "metadata": req.model_dump(),
                }
            )
            return {
                "is_success": False,
                "message": message,
            }

        if not existing_user.is_enabled:
            message = MESSAGES["AUTH"]["NOT_ENABLED"]
            self.logger.info(
                {
                    "activity_type": ACTIVITY_TYPES["USER_LOGIN"],
                    "message": message,
                    "metadata": req.model_dump(),
                }
            )
            return {
                "is_success": False,
                "message": message,
            }

        if existing_user.is_deleted:
            message = MESSAGES["AUTH"]["IS_DELETED"]
            self.logger.info(
                {
                    "activity_type": ACTIVITY_TYPES["USER_LOGIN"],
                    "message": message,
                    "metadata": req.model_dump(),
                }
            )
            return {
                "is_success": False,
                "message": message,
            }

        user = self.utility_service.sanitize_user_object(existing_user)
        self.logger.info(
            {
                "activity_type": ACTIVITY_TYPES["USER_LOGIN"],
                "message": MESSAGES["USER"]["SANITIZED"],
                "metadata": {"email": email},
            }
        )

        jwt_details = self.utility_service.generate_jwt(user.email, user.id)
        self.logger.info(
            {
                "activity_type": ACTIVITY_TYPES["USER_LOGIN"],
                "message": MESSAGES["COMMON"]["JWT_GENERATED"],
                "metadata": {"email": email},
            }
        )

        return {"is_success": True, "user": user, "token": jwt_details}

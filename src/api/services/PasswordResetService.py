from typing import Annotated

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.typing.UserSuccess import UserSuccess
from src.api.repositories.UserRepository import UserRepository
from src.api.repositories.PasswordResetRepository import PasswordResetRepository
from src.api.models.payload.requests.PasswordResetRequest import PasswordResetRequest

from .UtilityService import UtilityService


@Service()
class PasswordResetService:
    def __init__(
        self,
        logger: Annotated[Logger, "PasswordResetService"],
        utility_service: UtilityService,
    ) -> None:
        self.logger = logger
        self.utility_service = utility_service

    async def request_password_reset(self, req: PasswordResetRequest) -> UserSuccess:
        existing_user = await UserRepository.find_by_email(req.email)
        if not existing_user:
            self.logger.warn(
                {
                    "activity_type": "Request for password reset",
                    "message": "User doesn't exist",
                    "metadata": {"user": {"email": req.email}},
                }
            )
            return {
                "is_success": False,
                "message": "You don't have an account with us yet!",
            }
        elif not existing_user.is_active:
            self.logger.info(
                {
                    "activity_type": "Request for password reset",
                    "message": "User is not active",
                    "metadata": {"user": {"email": req.email}},
                }
            )
            return {
                "is_success": False,
                "message": "You can only reset the password of an active account!",
            }
        elif not existing_user.is_enabled:
            self.logger.info(
                {
                    "activity_type": "Request for password reset",
                    "message": "User is not enabled",
                    "metadata": {"user": {"email": req.email}},
                }
            )
            return {
                "is_success": False,
                "message": "You can only reset the password of an enabled account!",
            }
        password_reset_token = self.utility_service.generate_uuid()
        uuid = password_reset_token["uuid"]
        expires_at = password_reset_token["expires_at"]
        await PasswordResetRepository.set_new_password_reset_token(
            existing_user, uuid, expires_at
        )

        self.logger.info(
            {
                "activity_type": "Request for password reset",
                "message": "Password reset token set",
                "metadata": {"user": {"email": req.email}},
            }
        )
        return {
            "is_success": True,
            "message": f"Password reset email has been sent to {req.email}",
        }

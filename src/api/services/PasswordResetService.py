from typing import Annotated

from django.utils import timezone

from src.api.models.payload.requests.PasswordResetRequest import (
    ConfirmPasswordResetRequest, PasswordResetRequest)
from src.api.repositories.PasswordResetRepository import \
    PasswordResetRepository
from src.api.repositories.UserRepository import UserRepository
from src.api.typing.UserSuccess import UserSuccess
from src.utils.logger import Logger
from src.utils.svcs import Service

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
                "metadata": {"user": {"email": req.email}, "reset_token": existing_user.password_reset_token},
            }
        )
        return {
            "is_success": True,
            "message": f"Password reset email has been sent to {req.email}",
        }


    async def confirm_password_reset(self, req: ConfirmPasswordResetRequest) -> UserSuccess:
        existing_user = await UserRepository.find_by_reset_token(req.reset_token)
        if not existing_user:
            self.logger.warn(
                {
                    "activity_type": "Confirm password reset",
                    "message": "User doesn't exist",
                    "metadata": {"token": req.reset_token},
                }
            )
            return {
                "is_success": False,
                "message": "Invalid password reset token!",
            }
        elif not existing_user.is_active:
            self.logger.info(
                {
                    "activity_type": "Confirm password reset",
                    "message": "User is not active",
                    "metadata": {"token": req.reset_token},
                }
            )
            return {
                "is_success": False,
                "message": "You can only reset the password of an active account!",
            }
        elif not existing_user.is_enabled:
            self.logger.info(
                {
                    "activity_type": "Confirm password reset",
                    "message": "User is not enabled",
                    "metadata": {"token": req.reset_token},
                }
            )
            return {
                "is_success": False,
                "message": "You can only reset the password of an enabled account!",
            }

        if existing_user.token_expires_at < timezone.now():
            self.logger.warn(
                {
                    "activity_type": "Confirm password reset",
                    "message": "Token has expired",
                    "metadata": {"token": req.reset_token},
                }
            )
            return {
                "is_success": False,
                "message": "Password reset token has expired!",
            }
        new_password_hash = await self.utility_service.hash_string(req.new_password)
        await UserRepository.update_by_user(existing_user, {"password": new_password_hash})
        message = "Password reset successful!"
        self.logger.info(
            {
                "activity_type": "Confirm password reset",
                "message": message,
                "metadata": {"user": {"id": id}},
            }
        )

        return {"is_success": True, "message": message}
        
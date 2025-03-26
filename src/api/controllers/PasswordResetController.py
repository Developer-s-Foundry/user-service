from http import HTTPStatus
from typing import Annotated

from ninja.errors import HttpError

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.services.PasswordResetService import PasswordResetService
from src.api.models.payload.requests.PasswordResetRequest import PasswordResetRequest


@Service()
class PasswordResetController:
    def __init__(
        self,
        logger: Annotated[Logger, "PasswordResetController"],
        password_reset_service: PasswordResetService,
    ) -> None:
        self.logger = logger
        self.password_reset_service = password_reset_service

    async def request_password_reset(self, user_data: PasswordResetRequest) -> dict:
        try:
            sent_request = await self.password_reset_service.request_password_reset(
                user_data
            )
            return {"message": sent_request["message"]}
        except Exception as exc:
            if isinstance(exc, HttpError):
                raise
            self.logger.error(
                {
                    "activity_type": "Request for password reset",
                    "message": str(exc),
                    "metadata": user_data.model_dump(),
                }
            )
            raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, "Something went wrong")

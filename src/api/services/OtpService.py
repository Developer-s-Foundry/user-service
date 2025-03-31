from typing import Annotated
from datetime import timedelta

from src.env import otp
from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.typing.OTPSuccess import OTPSuccess
from src.api.constants.messages import MESSAGES
from src.api.constants.activity_types import ACTIVITY_TYPES
from src.api.repositories.OtpRepository import OtpRepository
from src.api.repositories.UserRepository import UserRepository

from .UtilityService import UtilityService

OTP_LIFETIME = timedelta(minutes=otp["lifetime"])


@Service()
class OtpService:
    def __init__(
        self, logger: Annotated[Logger, "OtpService"], utility_service: UtilityService
    ) -> None:
        self.logger = logger
        self.utility_service = utility_service

    async def send_otp(self, user_id: str) -> OTPSuccess:
        existing_user = await UserRepository.find_by_id(user_id)
        if not existing_user:
            message = MESSAGES["USER"]["DOESNT_EXIST"]
            self.logger.warn(
                {
                    "activity_type": ACTIVITY_TYPES["SEND_OTP"],
                    "message": message,
                    "metadata": {"user": {"id": user_id}},
                }
            )
            raise ValueError(message)

        if existing_user.is_validated:
            message = MESSAGES["OTP"]["USER_VALIDATED"]
            self.logger.info(
                {
                    "activity_type": ACTIVITY_TYPES["SEND_OTP"],
                    "message": message,
                    "metadata": {"user": {"id": user_id}},
                }
            )
            return {"is_success": False, "message": message}

        otp = await OtpRepository.find_valid_user_key(existing_user, OTP_LIFETIME)
        if not otp:
            key = self.utility_service.generate_random_string(
                length=6, numeric_only=True
            )
            otp = await OtpRepository.add(key, existing_user)

        otp  # Process the otp notification to the user

        message = MESSAGES["OTP"]["SEND_SUCCESS"]
        self.logger.info(
            {
                "activity_type": ACTIVITY_TYPES["SEND_OTP"],
                "message": message,
                "metadata": {"user": {"id": user_id}, "otp": {"key": otp.key}},
            }
        )
        return {"is_success": True, "message": message}

    async def validate_otp(self, user_id: str, key: str) -> bool:
        user = await UserRepository.find_by_id(user_id)
        if not user:
            self.logger.error(
                {
                    "activity_type": ACTIVITY_TYPES["VALIDATE_OTP"],
                    "message": MESSAGES["USER"]["DOESNT_EXIST"],
                    "metadata": {"user": {"id": user_id}},
                }
            )
            return False

        otp = await OtpRepository.find_valid_user_key(user, OTP_LIFETIME)
        if not otp:
            self.logger.info(
                {
                    "activity_type": ACTIVITY_TYPES["VALIDATE_OTP"],
                    "message": MESSAGES["OTP"]["VALIDATE_FAIL"],
                    "metadata": {"user": {"id": user_id}, "key": key},
                }
            )
            return False

        self.logger.info(
            {
                "activity_type": ACTIVITY_TYPES["VALIDATE_OTP"],
                "message": MESSAGES["OTP"]["VALIDATE_SUCCESS"],
                "metadata": {"user": {"id": user_id}, "key": key},
            }
        )
        return True

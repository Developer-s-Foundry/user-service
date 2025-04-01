from http import HTTPStatus
from typing import Annotated

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.constants.messages import DYNAMIC_MESSAGES
from src.api.utils.response_format import error_response, success_response
from src.api.services.UserKYCService import UserKYCService
from src.api.models.payload.requests.UserKYCRequest import UserKYCRequest


@Service()
class UserKYCController:
    def __init__(
        self,
        logger: Annotated[Logger, "UserKYCController"],
        kyc_service: UserKYCService,
    ) -> None:
        self.logger = logger
        self.kyc_service = kyc_service

    async def get_user_kyc(self, user_id: str) -> tuple:
        kyc = await self.kyc_service.fetch_details(user_id)
        return success_response(
            message=DYNAMIC_MESSAGES["COMMON"]["FETCHED_SUCCESS"]("KYC Information"),
            data=kyc,
            status_code=HTTPStatus.OK,
        )

    async def update_user_kyc(self, user_id: str, kyc_details: UserKYCRequest) -> tuple:
        updated_kyc = await self.kyc_service.update_details(user_id, kyc_details)
        if not updated_kyc["is_success"]:
            return error_response(
                message=updated_kyc["message"], status_code=HTTPStatus.BAD_REQUEST
            )
        return success_response(
            message=updated_kyc["message"], status_code=HTTPStatus.OK
        )

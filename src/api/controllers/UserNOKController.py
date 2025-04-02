from http import HTTPStatus
from typing import Annotated

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.constants.messages import DYNAMIC_MESSAGES
from src.api.utils.response_format import error_response, success_response
from src.api.services.UserNOKService import UserNOKService
from src.api.models.payload.requests.UserNOKRequest import UserNOKRequest


@Service()
class UserNOKController:
    def __init__(
        self,
        logger: Annotated[Logger, "UserNOKController"],
        nok_service: UserNOKService,
    ) -> None:
        self.logger = logger
        self.nok_service = nok_service

    async def get_user_nok(self, user_id: str) -> tuple:
        nok = await self.nok_service.fetch_details(user_id)
        return success_response(
            message=DYNAMIC_MESSAGES["COMMON"]["FETCHED_SUCCESS"]("Next of Kin"),
            data=nok,
            status_code=HTTPStatus.OK,
        )

    async def update_user_nok(self, user_id: str, nok_details: UserNOKRequest) -> tuple:
        updated_nok = await self.nok_service.update_details(user_id, nok_details)
        if not updated_nok["is_success"]:
            return error_response(
                message=updated_nok["message"], status_code=HTTPStatus.BAD_REQUEST
            )
        return success_response(
            message=updated_nok["message"], status_code=HTTPStatus.OK
        )

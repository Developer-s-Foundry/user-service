from typing import Annotated

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.typing.NOKSuccess import NOKSuccess
from src.api.constants.messages import MESSAGES
from src.api.constants.activity_types import ACTIVITY_TYPES
from src.api.repositories.UserRepository import UserRepository
from src.api.models.postgres.UserNextOfKin import UserNextOfKin
from src.api.repositories.UserNOKRepository import UserNOKRepository
from src.api.models.payload.requests.UserNOKRequest import UserNOKRequest


@Service()
class UserNOKService:
    def __init__(self, logger: Annotated[Logger, "UserNOKService"]) -> None:
        self.logger = logger

    async def update_details(
        self, user_id: str, nok_details: UserNOKRequest
    ) -> NOKSuccess:
        user = await UserRepository.find_by_id(user_id)
        if not user:
            self.logger.warn(
                {
                    "activity_type": ACTIVITY_TYPES["UPDATE_NOK"],
                    "message": MESSAGES["USER"]["DOESNT_EXIST"],
                    "metadata": {"user": {"id": user_id}},
                }
            )
            raise ValueError(MESSAGES["USER"]["DOESNT_EXIST"])
        nok = await UserNOKRepository.find_by_user(user)
        if not nok:
            nok = await UserNOKRepository.add(user, nok_details)
        else:
            nok = await UserNOKRepository.update(nok, nok_details)

        self.logger.info(
            {
                "activity_type": ACTIVITY_TYPES["UPDATE_NOK"],
                "message": MESSAGES["NOK"]["UPDATED"],
                "metadata": {"user": {"id": user_id}},
            }
        )
        return {"is_success": True, "message": MESSAGES["NOK"]["UPDATED"]}

    async def fetch_details(self, user_id: str) -> UserNextOfKin:
        user = await UserRepository.find_by_id(user_id)
        if not user:
            self.logger.warn(
                {
                    "activity_type": ACTIVITY_TYPES["FETCH_NOK"],
                    "message": MESSAGES["USER"]["DOESNT_EXIST"],
                    "metadata": {"user": {"id": user_id}},
                }
            )
            raise ValueError(MESSAGES["USER"]["DOESNT_EXIST"])
        nok = await UserNOKRepository.find_by_user(user)
        if not nok:
            nok = await UserNOKRepository.add(user, UserNOKRequest())

        self.logger.info(
            {
                "activity_type": ACTIVITY_TYPES["FETCH_NOK"],
                "message": MESSAGES["NOK"]["FETCHED"],
                "metadata": {"user": {"id": user_id}},
            }
        )
        return nok

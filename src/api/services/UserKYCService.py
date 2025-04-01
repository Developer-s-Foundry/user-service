from typing import Annotated

from src.utils.svcs import Service
from src.utils.logger import Logger
from src.api.models.postgres import UserKYCInformation
from src.api.constants.messages import MESSAGES
from src.api.typing.KYCInformaton import KYCSuccess, KYCValidation
from src.api.constants.activity_types import ACTIVITY_TYPES
from src.api.repositories.UserRepository import UserRepository
from src.api.repositories.UserKYCRepository import UserKYCRepository
from src.api.models.payload.requests.UserKYCRequest import UserKYCRequest


@Service()
class UserKYCService:
    def __init__(self, logger: Annotated[Logger, "UserKYCService"]) -> None:
        self.logger = logger

    async def update_details(
        self, user_id: str, kyc_details: UserKYCRequest
    ) -> KYCSuccess:
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
        kyc = await UserKYCRepository.find_by_user(user)
        if not kyc:
            kyc = await UserKYCRepository.add(user, kyc_details)

            # TODO: Validate the KYC

        else:
            updated_fields = kyc_details.model_fields_set
            extra: KYCValidation = {}
            if "bvn" in updated_fields and kyc_details.bvn != kyc.bvn:
                extra["is_bvn_verified"] = False
            if (
                "document_type" in updated_fields
                and kyc_details.document_type != kyc.document_type
            ) or (
                "document_id" in updated_fields
                and kyc_details.document_id != kyc.document_id
            ):
                extra["is_document_verified"] = False

            kyc = await UserKYCRepository.update(kyc, kyc_details, extra)

            if extra:
                # TODO: Validate the KYC
                ...

        self.logger.info(
            {
                "activity_type": ACTIVITY_TYPES["UPDATE_KYC"],
                "message": MESSAGES["KYC"]["UPDATED"],
                "metadata": {"user": {"id": user_id}},
            }
        )
        return {"is_success": True, "message": MESSAGES["KYC"]["UPDATED"]}

    async def fetch_details(self, user_id: str) -> UserKYCInformation:
        user = await UserRepository.find_by_id(user_id)
        if not user:
            self.logger.warn(
                {
                    "activity_type": ACTIVITY_TYPES["FETCH_KYC"],
                    "message": MESSAGES["USER"]["DOESNT_EXIST"],
                    "metadata": {"user": {"id": user_id}},
                }
            )
            raise ValueError(MESSAGES["USER"]["DOESNT_EXIST"])
        kyc = await UserKYCRepository.find_by_user(user)
        if not kyc:
            kyc = await UserKYCRepository.add(user, UserKYCRequest())

        self.logger.info(
            {
                "activity_type": ACTIVITY_TYPES["FETCH_KYC"],
                "message": MESSAGES["KYC"]["FETCHED"],
                "metadata": {"user": {"id": user_id}},
            }
        )
        return kyc

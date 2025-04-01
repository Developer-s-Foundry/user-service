from src.api.models.postgres import User, UserKYCInformation
from src.api.typing.KYCInformaton import KYCValidation
from src.api.models.payload.requests.UserKYCRequest import UserKYCRequest

from ._base import BaseRepository


class UserKYCRepository(BaseRepository[UserKYCInformation]):
    model = UserKYCInformation

    @classmethod
    async def add(cls, user: User, kyc_details: UserKYCRequest) -> UserKYCInformation:
        return await cls.manager.acreate(
            user=user, **kyc_details.model_dump(exclude_unset=True)
        )

    @classmethod
    async def find_by_user(cls, user: User) -> UserKYCInformation | None:
        return await cls.manager.filter(user=user).afirst()

    @classmethod
    async def update(
        cls,
        kyc: UserKYCInformation,
        kyc_details: UserKYCRequest,
        extra: KYCValidation | None = None,
    ) -> UserKYCInformation:
        for attr, value in kyc_details.model_dump(exclude_unset=True).items():
            setattr(kyc, attr, value)

        if extra:
            for attr, value in extra.items():
                setattr(kyc, attr, value)

        await kyc.asave()
        return kyc

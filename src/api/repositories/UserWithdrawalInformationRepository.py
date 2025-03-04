from ..models.postgres import UserWithdrawalInformation


class UserWithdrawalInformationRepository:
    @staticmethod
    async def add(user_account: UserWithdrawalInformation) -> UserWithdrawalInformation:
        await user_account.asave()
        return user_account

    @staticmethod
    async def find_by_id(id: str) -> UserWithdrawalInformation | None:
        return await UserWithdrawalInformation.objects.filter(id=id).afirst()

    @staticmethod
    async def list(user_id: str) -> list[UserWithdrawalInformation]:
        return await list(UserWithdrawalInformation.objects.filter(user__id=user_id))

    @staticmethod
    async def update_user_account(
        user_account_id: int, updates: dict | None = None
    ) -> None:
        user_account = await UserWithdrawalInformationRepository.find_by_id(
            user_account_id
        )

        if user_account and updates:
            for key, value in updates.items():
                setattr(user_account, key, value)
            await user_account.asave()

    @staticmethod
    async def delete_user_withdrawal_account(account_id: int) -> None:
        account = await UserWithdrawalInformationRepository.find_by_id(account_id)
        await account.adelete()

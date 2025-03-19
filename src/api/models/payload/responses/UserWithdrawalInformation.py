from ninja import ModelSchema

from src.api.models.postgres import (
    UserWithdrawalInformation as UserWithdrawalInformationModel,
)


class UserWithdrawalInformation(ModelSchema):
    class Meta:
        model = UserWithdrawalInformationModel
        fields = (
            "id",
            "user",
            "currency",
            "account_number",
            "account_name",
            "bank_code",
            "bank_name",
            "created_at",
            "last_updated_at",
        )

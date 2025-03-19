from ninja import ModelSchema

from src.api.models.postgres import Wallet as WalletModel


class Wallet(ModelSchema):
    class Meta:
        model = WalletModel
        fields = (
            "id",
            "account_number",
            "currency",
            "name",
            "tag",
            "daily_transaction_limit",
        )

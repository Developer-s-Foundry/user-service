from rest_framework import serializers

from src.api.enums.Currency import Currency


class AddWithdrawalAccountRequest(serializers.Serializer):
    user: str = None
    bank_name = serializers.CharField()
    bank_code = serializers.CharField()
    account_number = serializers.CharField()
    account_name = serializers.CharField()
    currency = serializers.ChoiceField(choices=Currency.choices, required=False)

    def validate(self, data: dict) -> dict:
        data["user"] = self.user
        return data

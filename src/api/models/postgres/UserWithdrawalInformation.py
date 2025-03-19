from django.db import models

from src.api.enums.Currency import Currency

from .User import User
from ._base import PostgresBaseModel


class UserWithdrawalInformation(PostgresBaseModel):
    id: models.BigAutoField = models.BigAutoField(primary_key=True)
    user: models.ForeignKey = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="withdrawal_informations"
    )
    currency: models.CharField = models.CharField(
        max_length=100, choices=Currency.choices, default=Currency.NGN
    )
    bank_code: models.CharField = models.CharField(max_length=10)
    bank_name: models.CharField = models.CharField(max_length=255)
    account_number: models.CharField = models.CharField(max_length=30)
    account_name: models.CharField = models.CharField(max_length=255)
    created_at: models.DateField = models.DateField(auto_now_add=True)
    last_updated_at: models.DateField = models.DateField(auto_now=True)

    class Meta:
        db_table = "users_withdrawal_information"

    def __str__(self) -> str:
        return str(self.id)

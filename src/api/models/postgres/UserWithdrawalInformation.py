from django.db import models

from api.enums.Currency import Currency

from .User import User


class UserWithdrawalInformation(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(
        User, related_name="", on_delete=models.SET_NULL, null=True
    )
    currency = models.CharField(
        max_length=100, choices=Currency.choices, default=Currency.NGN
    )
    bank_code = models.CharField(max_length=10)
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=30)
    account_name = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    last_updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return str(self.id)

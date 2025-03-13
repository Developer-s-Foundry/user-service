from typing import ClassVar
from decimal import Decimal

from django.db import models

from src.api.enums.Currency import Currency

from .User import User
from ._base import PostgresBaseModel


class Wallet(PostgresBaseModel):
    id: models.BigAutoField = models.BigAutoField(primary_key=True)
    user: models.ForeignKey = models.ForeignKey(
        User, related_name="wallets", on_delete=models.CASCADE
    )
    account_number: models.CharField = models.CharField(max_length=30, unique=True)
    currency: models.CharField = models.CharField(
        max_length=100, choices=Currency.choices, default=Currency.NGN
    )
    name: models.CharField = models.CharField(max_length=255)
    tag: models.CharField = models.CharField(max_length=100, null=True)
    daily_transaction_limit: models.DecimalField = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0"),  # 0 means no limit
    )
    is_active: models.BooleanField = models.BooleanField(default=True)
    is_enabled: models.BooleanField = models.BooleanField(default=True)
    created_at: models.DateField = models.DateField(auto_now_add=True)
    last_updated_at: models.DateField = models.DateField(auto_now=True)

    class Meta:
        indexes: ClassVar = [
            models.Index(fields=["account_number"]),
            models.Index(fields=["currency"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["is_enabled"]),
        ]

    def __str__(self) -> str:
        return str(self.id)

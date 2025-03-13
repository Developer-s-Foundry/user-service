from typing import ClassVar
from decimal import Decimal

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from ._base import PostgresBaseModel


class WalletLimit(PostgresBaseModel):
    id: models.BigAutoField = models.BigAutoField(primary_key=True)
    tier: models.IntegerField = models.IntegerField(
        default=1,
        unique=True,
        validators=[
            MinValueValidator(1, "Account tier is not valid"),
            MaxValueValidator(3, "Account tier is not valid"),
        ],
    )
    daily_transaction_limit: models.DecimalField = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("1")
    )
    total_balance_limit: models.DecimalField = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("1")
    )
    created_at: models.DateField = models.DateField(auto_now_add=True)
    last_updated_at: models.DateField = models.DateField(auto_now=True)

    class Meta:
        indexes: ClassVar = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["last_updated_at"]),
        ]

    def __str__(self) -> str:
        return str(self.id)

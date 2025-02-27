from typing import ClassVar

from django.db import models

from src.api.enums.Currency import Currency

from ._base import PostgresBaseModel


class Bank(PostgresBaseModel):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    currency = models.CharField(
        max_length=100, choices=Currency.choices, default=Currency.NGN
    )
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        indexes: ClassVar = [
            models.Index(fields=["code"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return str(self.id)

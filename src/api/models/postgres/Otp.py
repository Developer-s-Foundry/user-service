from django.db import models

from .User import User
from ._base import PostgresBaseModel


class Otp(PostgresBaseModel):
    id: models.BigAutoField = models.BigAutoField(primary_key=True)
    user: models.ForeignKey = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )
    key: models.CharField = models.CharField(max_length=255)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "otps"
        indexes = (
            models.Index(fields=["key"]),
            models.Index(fields=["created_at"]),
        )

    def __str__(self) -> str:
        return str(self.id)

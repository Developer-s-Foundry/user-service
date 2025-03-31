import uuid

from django.db import models

from ._base import PostgresBaseModel
from .StateLGA import StateLGA


class User(PostgresBaseModel):
    id: models.CharField = models.CharField(
        max_length=255,
        primary_key=True,
        default=uuid.uuid4,  # type: ignore
    )
    email: models.EmailField = models.EmailField(max_length=255, unique=True)
    password: models.CharField = models.CharField(max_length=255)
    first_name: models.CharField = models.CharField(max_length=255)
    last_name: models.CharField = models.CharField(max_length=255)
    address: models.CharField = models.CharField(max_length=255)
    phone_number: models.CharField = models.CharField(max_length=20)
    state_lga: models.ForeignKey = models.ForeignKey(
        StateLGA, on_delete=models.SET_NULL, null=True
    )
    profile_picture: models.CharField = models.CharField(max_length=255)
    tier: models.IntegerField = models.IntegerField(default=1)
    pin: models.CharField = models.CharField(max_length=10)
    password_reset_token: models.CharField = models.CharField(max_length=255)
    token_expires_at: models.DateTimeField = models.DateTimeField(null=True)
    is_validated: models.BooleanField = models.BooleanField(default=False)
    is_active: models.BooleanField = models.BooleanField(default=False)
    is_enabled: models.BooleanField = models.BooleanField(default=False)
    is_deleted: models.BooleanField = models.BooleanField(default=False)
    created_at: models.DateField = models.DateField(auto_now_add=True)
    last_updated_at: models.DateField = models.DateField(auto_now=True)

    class Meta:
        db_table = "users"
        indexes = (
            models.Index(fields=["first_name"]),
            models.Index(fields=["last_name"]),
            models.Index(fields=["tier"]),
            models.Index(fields=["is_validated"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["is_enabled"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["last_updated_at"]),
        )

    def __str__(self) -> str:
        return self.id

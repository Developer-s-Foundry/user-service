import uuid
from typing import ClassVar

from django.db import models

from ._base import PostgresBaseModel
from .StateLGA import StateLGA


class User(PostgresBaseModel):
    id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    state_lga = models.ForeignKey(StateLGA, on_delete=models.SET_NULL, null=True)
    profile_picture = models.CharField(max_length=255, null=True)
    tier = models.IntegerField(default=1)
    is_validated = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    last_updated_at = models.DateField(auto_now=True)

    class Meta:
        indexes: ClassVar = [
            models.Index(fields=["first_name"]),
            models.Index(fields=["last_name"]),
            models.Index(fields=["tier"]),
            models.Index(fields=["is_validated"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["is_enabled"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["last_updated_at"]),
        ]

    def __str__(self) -> str:
        return self.id

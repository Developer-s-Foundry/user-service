from typing import ClassVar

from django.db import models

from src.api.enums.NextOfKinRelationship import NextOfKinRelationship

from .User import User
from ._base import PostgresBaseModel


class UserNextOfKin(PostgresBaseModel):
    id: models.BigAutoField = models.BigAutoField(primary_key=True)
    user: models.OneToOneField = models.OneToOneField(
        User, related_name="next_of_kin", on_delete=models.SET_NULL, null=True
    )
    first_name: models.CharField = models.CharField(max_length=255, null=True)
    last_name: models.CharField = models.CharField(max_length=255, null=True)
    address: models.CharField = models.CharField(max_length=255, null=True)
    phone_number: models.CharField = models.CharField(max_length=20, null=True)
    email: models.EmailField = models.EmailField(max_length=255, null=True)
    relationship: models.CharField = models.CharField(
        max_length=20, choices=NextOfKinRelationship.choices, null=True
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

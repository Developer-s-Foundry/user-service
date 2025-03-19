from django.db import models

from src.api.enums.DocumentType import DocumentType

from .User import User
from ._base import PostgresBaseModel


class UserKYCInformation(PostgresBaseModel):
    id: models.BigAutoField = models.BigAutoField(primary_key=True)
    user: models.OneToOneField = models.OneToOneField(
        User, related_name="kyc", on_delete=models.SET_NULL, null=True
    )
    bvn: models.CharField = models.CharField(max_length=20, null=True)
    document_type: models.CharField = models.CharField(
        max_length=30, choices=DocumentType.choices, null=True
    )
    document_id: models.CharField = models.CharField(max_length=255, null=True)
    is_bvn_verified: models.BooleanField = models.BooleanField(default=False, null=True)
    is_document_verified: models.BooleanField = models.BooleanField(
        default=False, null=True
    )
    created_at: models.DateField = models.DateField(auto_now_add=True)
    last_updated_at: models.DateField = models.DateField(auto_now=True)

    class Meta:
        db_table = "users_kyc_information"
        indexes = (
            models.Index(fields=["is_bvn_verified"]),
            models.Index(fields=["is_document_verified"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["last_updated_at"]),
        )

    def __str__(self) -> str:
        return str(self.id)

from django.db import models

from ._base import PostgresBaseModel


class StateLGA(PostgresBaseModel):
    id: models.BigAutoField = models.BigAutoField(primary_key=True)
    state: models.CharField = models.CharField(max_length=100)
    lga: models.CharField = models.CharField(max_length=100)
    created_at: models.DateField = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "state_lgas"
        indexes = (models.Index(fields=["state"]),)

    def __str__(self) -> str:
        return str(self.id)

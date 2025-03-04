from django.db import models


class PostgresBaseModel(models.Model):
    class Meta:
        app_label = "postgres"
        abstract = True

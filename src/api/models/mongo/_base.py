from django.db import models


class MongoBaseModel(models.Model):
    class Meta:
        app_label = "mongo"
        abstract = True

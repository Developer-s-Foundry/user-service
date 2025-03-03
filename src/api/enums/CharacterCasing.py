from django.db import models


class CharacterCasing(models.TextChoices):
    LOWER = "lower"
    UPPER = "upper"
    MIXED = "mixed"

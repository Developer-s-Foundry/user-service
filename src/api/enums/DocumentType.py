from django.db import models


class DocumentType(models.TextChoices):
    INTL_PASSPORT = "Int'l Passport"
    VOTERS_CARD = "Voter's Card"
    DRIVERS_LICENCE = "Driver's Licence"
    NIN = "NIN"

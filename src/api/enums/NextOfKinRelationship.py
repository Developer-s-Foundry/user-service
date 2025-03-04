from django.db import models


class NextOfKinRelationship(models.TextChoices):
    FATHER = "father"
    MOTHER = "mother"
    BROTHER = "brother"
    SISTER = "sister"
    UNCLE = "uncle"
    AUNT = "aunt"
    COUSIN = "cousin"
    NEPHEW = "nephew"
    NIECE = "niece"
    SON = "son"
    DAUGHTER = "daughter"

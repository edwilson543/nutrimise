# Django imports
from django.db import models as django_models


class Nutrient(django_models.Model):
    """
    Some nutrient, e.g. protein.
    """

    name = django_models.TextField(unique=True)

    def __str__(self) -> str:
        return self.name

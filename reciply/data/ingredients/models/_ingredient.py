# Django imports
from django.db import models as django_models


class Ingredient(django_models.Model):
    """
    Some ingredient and its nutritional information.
    """

    name_singular = django_models.CharField(max_length=128)

    name_plural = django_models.CharField(max_length=128)

    category = django_models.CharField(max_length=128)

    displayed_units_singular = django_models.CharField(max_length=64, null=True)

    displayed_units_plural = django_models.CharField(max_length=64, null=True)

    # Conversion factor (e.g. for calculating nutritional information per apple)

    grams_per_displayed_unit = django_models.FloatField()

    # Nutritional information

    protein_per_gram = django_models.FloatField()

    carbohydrates_per_gram = django_models.FloatField()

    def __str__(self) -> str:
        return self.name_singular

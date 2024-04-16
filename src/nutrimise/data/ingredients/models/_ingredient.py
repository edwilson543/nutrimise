from django.db import models as django_models

from . import _dietary_requirement


class IngredientCategory(django_models.Model):
    """
    A category of ingredients.
    """

    id = django_models.AutoField(primary_key=True)
    name = django_models.TextField(unique=True)

    def __str__(self) -> str:
        return self.name


class Ingredient(django_models.Model):
    """
    Some ingredient and its nutritional information.
    """

    name = django_models.CharField(max_length=128, unique=True)

    category = django_models.ForeignKey(
        IngredientCategory, on_delete=django_models.PROTECT, related_name="ingredients"
    )

    units = django_models.CharField(max_length=64, null=True, blank=True)

    # Conversion factor (e.g. for calculating nutritional information per apple)
    grams_per_unit = django_models.FloatField()

    dietary_requirements_satisfied = django_models.ManyToManyField(  # type: ignore[var-annotated]
        _dietary_requirement.DietaryRequirement, related_name="ingredients", blank=True
    )

    def __str__(self) -> str:
        return self.name

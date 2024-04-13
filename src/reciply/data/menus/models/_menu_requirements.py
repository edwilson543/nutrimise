from django.db import models as django_models

from reciply.data import constants

from . import _menu


class MenuRequirements(django_models.Model):
    """
    The requirements to meet when optimising a menu.
    """

    menu = django_models.OneToOneField(
        _menu.Menu, on_delete=django_models.CASCADE, related_name="requirements"
    )

    maximum_occurrences_per_recipe = django_models.SmallIntegerField()

    # TODO -> dietary requirements M2M field.


class NutrientRequirement(django_models.Model):
    """
    The nutrient requirements to meet when optimising a menu.
    """

    id = django_models.AutoField(primary_key=True)

    menu_requirements = django_models.ForeignKey(
        MenuRequirements,
        on_delete=django_models.CASCADE,
        related_name="nutrient_requirements",
    )

    nutrient = django_models.ForeignKey(
        "ingredients.Nutrient", on_delete=django_models.PROTECT, related_name="+"
    )

    minimum_grams = django_models.FloatField(null=True)

    maximum_grams = django_models.FloatField(null=True)

    target_grams = django_models.FloatField(null=True)

    enforcement_interval = django_models.TextField(
        choices=constants.NutrientRequirementEnforcementInterval.choices
    )

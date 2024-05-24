import enum

from django.db import models as django_models


class MediaNamespace(enum.StrEnum):
    """
    Namespace for accessing certain types of media files in storage.
    """

    RECIPES = "recipes"


class MealTime(django_models.TextChoices):
    BREAKFAST = "BREAKFAST", "Breakfast"
    LUNCH = "LUNCH", "Lunch"
    DINNER = "DINNER", "Dinner"


class NutrientRequirementEnforcementInterval(django_models.TextChoices):
    DAILY = "DAILY", "Daily"


class NutrientUnit(django_models.TextChoices):
    GRAMS = "GRAMS", "Grams"

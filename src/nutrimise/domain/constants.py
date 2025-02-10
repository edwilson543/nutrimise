from django.db import models as django_models


class NutrientRequirementEnforcementInterval(django_models.TextChoices):
    DAILY = "DAILY", "Daily"

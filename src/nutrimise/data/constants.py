from django.db import models as django_models


class MealTime(django_models.TextChoices):
    BREAKFAST = "BREAKFAST", "Breakfast"
    LUNCH = "LUNCH", "Lunch"
    DINNER = "DINNER", "Dinner"

    def order(self) -> int:
        ordering = {
            self.BREAKFAST: 0,
            self.LUNCH: 1,
            self.DINNER: 2,
        }
        return ordering[self]  # type:ignore[index]


class NutrientRequirementEnforcementInterval(django_models.TextChoices):
    DAILY = "DAILY", "Daily"


class NutrientUnit(django_models.TextChoices):
    GRAMS = "GRAMS", "Grams"

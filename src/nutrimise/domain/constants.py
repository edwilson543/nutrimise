from django.db import models as django_models


EMBEDDING_DIMENSIONS = 1024


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


class OptimisationMode(django_models.TextChoices):
    RANDOM = "RANDOM", "Random"
    NUTRIENT = "NUTRIENT", "Nutrient"
    VARIETY = "VARIETY", "Ingredient variety"
    EVERYTHING = "EVERYTHING", "Everything"


class NutrientRequirementEnforcementInterval(django_models.TextChoices):
    DAILY = "DAILY", "Daily"


class NutrientUnit(django_models.TextChoices):
    GRAMS = "GRAMS", "Grams"
    KCAL = "KCAL", "kcal"


class EmbeddingVendor(django_models.TextChoices):
    OPEN_AI = "OPEN_AI"

    # Fakes. - todo.
    FAKE = "FAKE"
    FAKE_NO_SERVICE = "FAKE_NO_SERVICE"
    FAKE_NO_MODEL = "FAKE_NO_MODEL"


class EmbeddingModel(django_models.TextChoices):
    # OpenAI.
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    FAKE = "fake"

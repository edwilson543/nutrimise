from __future__ import annotations

import attrs
from django.db import models as django_models

from nutrimise.domain import embeddings, ingredients


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


@attrs.frozen
class Recipe:
    id: int
    name: str
    description: str
    methodology: str
    meal_times: tuple[MealTime, ...]
    # The absolute amount of each nutrient, per serving.
    nutritional_information_per_serving: tuple[ingredients.NutritionalInformation, ...]
    ingredients: tuple[RecipeIngredient, ...]
    embeddings: tuple[embeddings.Embedding, ...]

    # Queries
    def nutrient_quantity_per_serving(self, *, nutrient_id: int) -> float:
        for nutritional_information in self.nutritional_information_per_serving:
            if nutritional_information.nutrient.id == nutrient_id:
                return nutritional_information.nutrient_quantity
        return 0

    @property
    def unique_ingredient_ids(self) -> tuple[int, ...]:
        return tuple({ingredient.ingredient.id for ingredient in self.ingredients})


@attrs.frozen
class RecipeIngredient:
    ingredient: ingredients.Ingredient
    quantity: float


@attrs.frozen
class RecipeAuthor:
    id: int
    first_name: str
    last_name: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

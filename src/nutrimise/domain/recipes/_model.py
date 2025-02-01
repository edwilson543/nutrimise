from __future__ import annotations

import attrs

from nutrimise.domain import constants, ingredients


@attrs.frozen
class Recipe:
    id: int
    meal_times: tuple[constants.MealTime, ...]
    nutritional_information_per_serving: tuple[ingredients.NutritionalInformation, ...]
    """
    The absolute amount of each nutrient, per serving.
    """
    ingredients: tuple[RecipeIngredient, ...]

    # Queries
    def nutrient_quantity_per_serving(self, *, nutrient_id: int) -> float:
        for nutritional_information in self.nutritional_information_per_serving:
            if nutritional_information.nutrient.id == nutrient_id:
                return nutritional_information.nutrient_quantity
        return 0

    @property
    def unique_ingredient_ids(self) -> tuple[int, ...]:
        return tuple({ingredient.ingredient_id for ingredient in self.ingredients})


@attrs.frozen
class RecipeIngredient:
    ingredient_id: int

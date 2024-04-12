from __future__ import annotations

import attrs

from reciply.data import constants
from reciply.data.recipes import models as recipe_models
from reciply.domain import ingredients


@attrs.frozen
class Recipe:
    id: int
    meal_times: tuple[constants.MealTime, ...]
    nutritional_information_per_serving: tuple[ingredients.NutritionalInformation, ...]
    """
    The absolute amount of each nutrient, per serving.
    """

    @classmethod
    def from_orm_model(cls, *, recipe: recipe_models.Recipe) -> Recipe:
        nutritional_information = ingredients.get_nutritional_information_for_recipe(
            recipe=recipe, per_serving=True
        )
        return cls(
            id=recipe.id,
            meal_times=tuple(
                constants.MealTime(meal_time) for meal_time in recipe.meal_times
            ),
            nutritional_information_per_serving=tuple(nutritional_information),
        )

    # Queries
    def nutrient_grams_per_serving(self, *, nutrient_id: int) -> float:
        for nutritional_information in self.nutritional_information_per_serving:
            if nutritional_information.nutrient.id == nutrient_id:
                return nutritional_information.nutrient_quantity_grams
        return 0

from __future__ import annotations

# Standard library imports
import dataclasses

# Local application imports
from reciply.data import constants
from reciply.data.recipes import models as recipe_models
from reciply.domain import ingredients


@dataclasses.dataclass(frozen=True)
class Recipe:
    id: int
    meal_times: tuple[constants.MealTime]
    nutritional_information: tuple[ingredients.NutritionalInformation]

    @classmethod
    def from_orm_model(cls, *, recipe: recipe_models.Recipe) -> Recipe:
        nutritional_information = ingredients.get_nutritional_information_for_recipe(
            recipe=recipe, per_serving=True
        )
        return cls(
            id=recipe.id,
            meal_times=tuple(constants.MealTime(meal_time) for meal_time in recipe.meal_times),
            nutritional_information=tuple(nutritional_information),
        )

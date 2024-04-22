from __future__ import annotations

import attrs

from nutrimise.data import constants
from nutrimise.data.recipes import models as recipe_models
from nutrimise.domain import ingredients


@attrs.frozen
class Recipe:
    id: int
    meal_times: tuple[constants.MealTime, ...]
    nutritional_information_per_serving: tuple[ingredients.NutritionalInformation, ...]
    """
    The absolute amount of each nutrient, per serving.
    """
    ingredients: tuple[RecipeIngredient, ...]

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
            ingredients=RecipeIngredient.from_orm_model(
                recipe_ingredients=list(recipe.ingredients.all())
            ),
        )

    # Queries
    def nutrient_quantity_per_serving(self, *, nutrient_id: int) -> float:
        for nutritional_information in self.nutritional_information_per_serving:
            if nutritional_information.nutrient.id == nutrient_id:
                return nutritional_information.nutrient_quantity
        return 0


@attrs.frozen
class RecipeIngredient:
    ingredient_id: int

    @classmethod
    def from_orm_model(
        cls, *, recipe_ingredients: list[recipe_models.RecipeIngredient]
    ) -> tuple[RecipeIngredient, ...]:
        return tuple(
            cls(ingredient_id=recipe_ingredient.ingredient_id)
            for recipe_ingredient in recipe_ingredients
        )

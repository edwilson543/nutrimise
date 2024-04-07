from __future__ import annotations

# Standard library imports
import collections
import dataclasses

# Local application imports
from reciply.data.recipes import models as recipe_models


@dataclasses.dataclass
class NutritionalInformation:
    nutrient_name: str
    nutrient_quantity_grams: float


def get_nutritional_information_for_recipe(
    *, recipe: recipe_models.Recipe, per_serving: bool
) -> list[NutritionalInformation]:
    """
    Return a list of all the nutrients in a recipe and their quantities.
    """

    recipe_nutrition: collections.defaultdict[str, float] = collections.defaultdict(
        float
    )

    for recipe_ingredient in recipe.ingredients.all():
        grams_of_ingredient = recipe_ingredient.grams()
        for (
            ingredient_nutrition
        ) in recipe_ingredient.ingredient.nutritional_information.all():
            grams_of_nutrient = (
                grams_of_ingredient * ingredient_nutrition.quantity_per_gram
            )
            recipe_nutrition[ingredient_nutrition.nutrient.name] += grams_of_nutrient

    per_serving_denominator = recipe.number_of_servings if per_serving else 1
    recipe_nutrition_list = [
        NutritionalInformation(
            nutrient_name=nutrient,
            nutrient_quantity_grams=grams / per_serving_denominator,
        )
        for nutrient, grams in recipe_nutrition.items()
    ]
    return sorted(recipe_nutrition_list, key=lambda n: n.nutrient_name)

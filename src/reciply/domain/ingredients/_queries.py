from __future__ import annotations

# Standard library imports
import collections

# Local application imports
from reciply.data.ingredients import models as ingredient_models
from reciply.data.recipes import models as recipe_models

from . import _model


def get_nutritional_information_for_recipe(
    *, recipe: recipe_models.Recipe, per_serving: bool
) -> list[_model.NutritionalInformation]:
    """
    Return a list of all the nutrients in a recipe and their quantities.
    """

    recipe_nutrition: collections.defaultdict[_model.Nutrient, float] = (
        collections.defaultdict(float)
    )
    per_serving_denominator = recipe.number_of_servings if per_serving else 1

    for recipe_ingredient in recipe.ingredients.all():
        grams_of_ingredient = recipe_ingredient.grams()
        for (
            ingredient_nutrition
        ) in recipe_ingredient.ingredient.nutritional_information.all():
            nutrient_quantity_grams = (
                grams_of_ingredient
                * ingredient_nutrition.quantity_per_gram
                / per_serving_denominator
            )
            nutrient = _model.Nutrient(
                id=ingredient_nutrition.nutrient.id,
                name=ingredient_nutrition.nutrient.name,
            )
            recipe_nutrition[nutrient] += nutrient_quantity_grams

    nutritional_information = (
        _model.NutritionalInformation(
            nutrient=nutrient,
            nutrient_quantity_grams=value,
        )
        for nutrient, value in recipe_nutrition.items()
    )
    return sorted(nutritional_information, key=lambda n: n.nutrient.name)


def get_ingredient_display_name(
    *, ingredient: ingredient_models.Ingredient, quantity: float
) -> str:
    is_integer = quantity == int(quantity)
    if is_integer:
        quantity = int(quantity)
    else:
        quantity = round(quantity, 2)

    if ingredient.units:
        return f"{quantity} {ingredient.units} of {ingredient.name_singular}"
    else:
        if quantity == 1:
            return f"{quantity} {ingredient.name_singular}"
        else:
            return f"{quantity} {ingredient.name_plural}"

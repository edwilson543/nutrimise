from __future__ import annotations


import collections

from nutrimise.data import constants
from nutrimise.data.recipes import models as recipe_models

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
            nutrient_quantity = (
                grams_of_ingredient
                * ingredient_nutrition.quantity_per_gram
                / per_serving_denominator
            )
            nutrient = _model.Nutrient(
                id=ingredient_nutrition.nutrient.id,
                name=ingredient_nutrition.nutrient.name,
            )
            recipe_nutrition[nutrient] += nutrient_quantity

    nutritional_information = (
        _model.NutritionalInformation(
            nutrient=nutrient,
            nutrient_quantity=value,
            units=constants.NutrientUnit.GRAMS,
        )
        for nutrient, value in recipe_nutrition.items()
    )
    return sorted(nutritional_information, key=lambda n: n.nutrient.name)

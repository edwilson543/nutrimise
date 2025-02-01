from __future__ import annotations

import collections

from collections import abc as collections_abc

from nutrimise.data.ingredients import models as ingredient_models
from nutrimise.data.menus import models as menu_models
from nutrimise.data.recipes import models as recipe_models
from nutrimise.domain import constants
from nutrimise.domain.ingredients import _model


def get_ingredients(
    *, ingredient_ids: collections_abc.Iterable[int]
) -> tuple[_model.Ingredient, ...]:
    ingredients = ingredient_models.Ingredient.objects.filter(id__in=ingredient_ids)
    return tuple(ingredient.to_domain_model() for ingredient in ingredients)


def get_nutritional_information_for_menu_per_day(
    *, menu: menu_models.Menu, per_serving: bool
) -> dict[int, list[_model.NutritionalInformation]]:
    """
    Return a list of all the nutrients in a menu and their quantities, per day.

    Note that the same set of nutrients is included for each day, even if that nutrient
    is not included in any of the recipes on that day.
    """
    unaggregated_information: collections.defaultdict[
        int, list[_model.NutritionalInformation]
    ] = collections.defaultdict(list)
    nutrients: set[_model.Nutrient] = set()

    for menu_item in menu.items.all():
        if (recipe := menu_item.recipe) is not None:
            nutritional_information = get_nutritional_information_for_recipe(
                recipe=recipe, per_serving=per_serving
            )
            unaggregated_information[menu_item.day].extend(nutritional_information)

            # Collect the unique set of ingredients.
            for information in nutritional_information:
                nutrients.add(information.nutrient)

    ordered_nutrients = list(sorted(nutrients, key=lambda nutrient: nutrient.name))
    return {
        day: _model.NutritionalInformation.sum_by_nutrient(
            nutritional_information=nutritional_information, nutrients=ordered_nutrients
        )
        for day, nutritional_information in unaggregated_information.items()
    }


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

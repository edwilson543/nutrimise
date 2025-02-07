from collections.abc import Iterable

import factory

from nutrimise.domain import constants, recipes
from nutrimise.domain import ingredients as ingredients_domain

from . import _ingredients


class Recipe(factory.Factory):
    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f"recipe-{n}")
    description = factory.Sequence(lambda n: f"description-{n}")
    meal_times = factory.LazyFunction(tuple)
    nutritional_information_per_serving = factory.LazyFunction(tuple)
    ingredients = factory.LazyFunction(tuple)
    embeddings = factory.LazyFunction(tuple)

    class Meta:
        model = recipes.Recipe

    @classmethod
    def any_meal_time_with_nutrient(
        cls, *, nutrient: ingredients_domain.Nutrient, nutrient_quantity: float
    ) -> recipes.Recipe:
        high_nutrition = _ingredients.NutritionalInformation(
            nutrient=nutrient, nutrient_quantity=nutrient_quantity
        )
        return cls.create(
            nutritional_information_per_serving=(high_nutrition,),
            meal_times=[meal_time for meal_time in constants.MealTime],
        )

    @classmethod
    def with_ingredients(
        cls, *, ingredients: Iterable[ingredients_domain.Ingredient], **kwargs: object
    ) -> recipes.Recipe:
        recipe_ingredients = tuple(
            RecipeIngredient(ingredient=ingredient) for ingredient in ingredients
        )
        return cls.create(ingredients=recipe_ingredients, **kwargs)


class RecipeIngredient(factory.Factory):
    ingredient = factory.SubFactory(_ingredients.Ingredient)
    quantity = 2.5

    class Meta:
        model = recipes.RecipeIngredient

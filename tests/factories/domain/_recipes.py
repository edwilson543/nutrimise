import factory
from reciply.data import constants
from reciply.domain import recipes, ingredients

from . import _ingredients


class Recipe(factory.Factory):
    id = factory.Sequence(lambda n: n)
    meal_times = factory.LazyFunction(tuple)
    nutritional_information_per_serving = factory.LazyFunction(tuple)

    class Meta:
        model = recipes.Recipe

    @classmethod
    def any_meal_time_with_nutrient(
        cls, *, nutrient: ingredients.Nutrient, nutrient_quantity_grams: int
    ) -> recipes.Recipe:
        high_nutrition = _ingredients.NutritionalInformation(
            nutrient=nutrient, nutrient_quantity_grams=nutrient_quantity_grams
        )
        return cls.create(
            nutritional_information_per_serving=(high_nutrition,),
            meal_times=[meal_time for meal_time in constants.MealTime],
        )

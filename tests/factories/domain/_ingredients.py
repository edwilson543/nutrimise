import factory

from nutrimise.data import constants
from nutrimise.domain import ingredients


class Ingredient(factory.Factory):
    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f"ingredient-{n}")
    category_id = factory.Sequence(lambda n: n)

    class Meta:
        model = ingredients.Ingredient


class Nutrient(factory.Factory):
    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f"nutrient-{n}")

    class Meta:
        model = ingredients.Nutrient


class NutritionalInformation(factory.Factory):
    nutrient = factory.SubFactory(Nutrient)
    nutrient_quantity = 1
    units = constants.NutrientUnit.GRAMS

    class Meta:
        model = ingredients.NutritionalInformation

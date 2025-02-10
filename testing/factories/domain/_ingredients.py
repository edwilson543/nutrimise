import factory

from nutrimise.domain import ingredients


class IngredientCategory(factory.Factory):
    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f"ingredient-category-{n}")

    class Meta:
        model = ingredients.IngredientCategory


class Ingredient(factory.Factory[ingredients.Ingredient]):
    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f"ingredient-{n}")
    category = factory.SubFactory(IngredientCategory)
    units = factory.Sequence(lambda n: f"units-{n}")
    grams_per_unit = 1.0

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
    units = ingredients.NutrientUnit.GRAMS

    class Meta:
        model = ingredients.NutritionalInformation

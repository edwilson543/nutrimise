import factory
from reciply.data import constants
from reciply.data.ingredients import models as ingredient_models


class IngredientCategory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"ingredient-category-{n}")

    class Meta:
        model = ingredient_models.IngredientCategory


class Ingredient(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"ingredient-{n}")
    category = factory.SubFactory(IngredientCategory)
    grams_per_unit = 1

    class Meta:
        model = ingredient_models.Ingredient


class Nutrient(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"nutrient-{n}")

    class Meta:
        model = ingredient_models.Nutrient


class IngredientNutritionalInformation(factory.django.DjangoModelFactory):
    ingredient = factory.SubFactory(Ingredient)
    nutrient = factory.SubFactory(Nutrient)
    quantity_per_gram = 0.5
    units = constants.NutrientUnit

    class Meta:
        model = ingredient_models.IngredientNutritionalInformation

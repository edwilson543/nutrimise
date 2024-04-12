import factory
from reciply.data.ingredients import models as ingredient_models


class Ingredient(factory.django.DjangoModelFactory):
    name_singular = factory.Sequence(lambda n: f"ingredient-{n}")
    name_plural = factory.Sequence(lambda n: f"ingredient-{n}s")
    category = "Meat"
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

    class Meta:
        model = ingredient_models.IngredientNutritionalInformation

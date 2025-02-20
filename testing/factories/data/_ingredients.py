import factory

from nutrimise.data.ingredients import models as ingredient_models
from nutrimise.domain import ingredients


class DietaryRequirement(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"dietary-requirement-{n}")

    class Meta:
        model = ingredient_models.DietaryRequirement


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
    units = ingredients.NutrientUnit.GRAMS.value

    class Meta:
        model = ingredient_models.Nutrient


class IngredientNutritionalInformation(factory.django.DjangoModelFactory):
    ingredient = factory.SubFactory(Ingredient)
    nutrient = factory.SubFactory(Nutrient)
    quantity_per_gram = 0.5

    class Meta:
        model = ingredient_models.IngredientNutritionalInformation

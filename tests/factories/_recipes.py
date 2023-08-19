# Third party imports
import factory

# Local application imports
from data.recipes import models as recipe_models

from . import _auth, _ingredients


class Recipe(factory.django.DjangoModelFactory):
    author = factory.SubFactory(_auth.User)
    name = factory.Sequence(lambda n: f"recipe-{n}")
    description = "Some description"

    class Meta:
        model = recipe_models.Recipe


class RecipeImage(factory.django.DjangoModelFactory):
    recipe = factory.SubFactory(Recipe)
    is_hero = False

    class Meta:
        model = recipe_models.RecipeImage


class RecipeIngredient(factory.django.DjangoModelFactory):
    recipe = factory.SubFactory(Recipe)
    ingredient = factory.SubFactory(_ingredients.Ingredient)
    quantity = 1.0

    class Meta:
        model = recipe_models.RecipeIngredient

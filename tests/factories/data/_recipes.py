from typing import Any

import factory

from nutrimise.data.ingredients import models as ingredient_models
from nutrimise.data.recipes import models as recipe_models
from nutrimise.domain import constants, embeddings

from . import _auth, _ingredients


class Recipe(factory.django.DjangoModelFactory):
    author = factory.SubFactory(_auth.User)
    name = factory.Sequence(lambda n: f"recipe-{n}")
    description = "Some description"
    meal_times = [constants.MealTime.DINNER.value]
    number_of_servings = 2

    class Meta:
        model = recipe_models.Recipe

    @classmethod
    def create_to_satisfy_dietary_requirements(
        cls,
        dietary_requirements: tuple[ingredient_models.DietaryRequirement, ...],
        **kwargs: Any,
    ) -> recipe_models.Recipe:
        """
        Create a recipe whose only ingredient satisfied the requirements.
        """
        ingredient = _ingredients.Ingredient()
        ingredient.dietary_requirements_satisfied.add(*dietary_requirements)

        recipe = cls(**kwargs)
        RecipeIngredient(recipe=recipe, ingredient=ingredient)
        return recipe


class RecipeIngredient(factory.django.DjangoModelFactory):
    recipe = factory.SubFactory(Recipe)
    ingredient = factory.SubFactory(_ingredients.Ingredient)
    quantity = 1.0

    class Meta:
        model = recipe_models.RecipeIngredient


class RecipeEmbedding(factory.django.DjangoModelFactory):
    recipe = factory.SubFactory(Recipe)
    vector = factory.LazyFunction(lambda: RecipeEmbedding.stub_vector())
    vendor = embeddings.EmbeddingVendor.FAKE.value
    model = embeddings.EmbeddingModel.FAKE.value

    class Meta:
        model = recipe_models.RecipeEmbedding

    @staticmethod
    def stub_vector() -> list[float]:
        return [1.0] + [0] * (embeddings.EMBEDDING_DIMENSIONS - 1)

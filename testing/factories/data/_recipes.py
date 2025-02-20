from typing import Any

import factory

from nutrimise.data.ingredients import models as ingredient_models
from nutrimise.data.recipes import models as recipe_models
from nutrimise.domain import embeddings, recipes

from . import _ingredients


class RecipeAuthor(factory.django.DjangoModelFactory):
    first_name = factory.Sequence(lambda n: f"first-name-{n}")
    last_name = factory.Sequence(lambda n: f"last-name-{n}")

    class Meta:
        model = recipe_models.RecipeAuthor


class Recipe(factory.django.DjangoModelFactory):
    author = factory.SubFactory(RecipeAuthor)
    name = factory.Sequence(lambda n: f"recipe-{n}")
    description = factory.Sequence(lambda n: f"description-{n}")
    methodology = factory.Sequence(lambda n: f"methodology-{n}")
    meal_times = [recipes.MealTime.DINNER.value]
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
        ingredient = _ingredients.Ingredient.create()
        ingredient.dietary_requirements_satisfied.add(*dietary_requirements)

        recipe = cls.create(**kwargs)
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
    vector = factory.LazyFunction(embeddings.get_stub_vector_embedding)
    prompt_hash = factory.Sequence(lambda n: f"embedded-content-hash-{n}")
    vendor = embeddings.EmbeddingVendor.FAKE.value
    model = embeddings.EmbeddingModel.FAKE.value

    class Meta:
        model = recipe_models.RecipeEmbedding

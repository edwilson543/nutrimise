import uuid

from django.contrib.auth import models as auth_models

from nutrimise.domain import constants, embeddings

from . import models as recipe_models


def create_or_update_recipe_embedding(
    *, recipe_id: int, embedding: embeddings.Embedding
) -> None:
    recipe_models.RecipeEmbedding.objects.update_or_create(
        recipe_id=recipe_id,
        model=embedding.model.value,
        vendor=embedding.vendor.value,
        defaults={
            "vector": embedding.vector,
            "prompt_hash": embedding.prompt_hash,
        },
    )


def create_recipe(
    *,
    author: auth_models.User,
    name: str,
    description: str,
    meal_times: list[constants.MealTime],
    number_of_servings: int,
) -> int:
    if recipe_models.Recipe.objects.filter(author_id=author.id, name=name).exists():
        name += f" (duplicate {uuid.uuid4()})"

    recipe = recipe_models.Recipe.objects.create(
        author_id=author.id,
        name=name,
        description=description,
        meal_times=meal_times,
        number_of_servings=number_of_servings,
    )
    return recipe.id

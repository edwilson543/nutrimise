from django.contrib.auth import models as auth_models

from nutrimise.domain import embeddings

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


def create_recipe(*, name: str, description: str, author: auth_models.User) -> int:
    # TODO -> create or update recipe?
    recipe = recipe_models.Recipe.objects.create(
        author_id=author.id,
        name=name,
        description=description,
        meal_times=["DINNER"],
        number_of_servings=2,
    )
    return recipe.id

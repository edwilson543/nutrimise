import uuid

from nutrimise.domain import embeddings, recipes

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
    author: recipes.RecipeAuthor | None,
    name: str,
    description: str,
    methodology: str,
    meal_times: list[recipes.MealTime],
    number_of_servings: int,
    recipe_ingredients: list[recipes.RecipeIngredient],
) -> int:
    author_id = author.id if author else None

    if recipe_models.Recipe.objects.filter(author_id=author_id, name=name).exists():
        name += f" (duplicate {uuid.uuid4()})"

    recipe = recipe_models.Recipe.objects.create(
        author_id=author_id,
        name=name,
        description=description,
        methodology=methodology,
        meal_times=meal_times,
        number_of_servings=number_of_servings,
    )

    recipe_ingredients_to_create = [
        recipe_models.RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=recipe_ingredient.ingredient.id,
            quantity=recipe_ingredient.quantity,
        )
        for recipe_ingredient in recipe_ingredients
    ]
    recipe_models.RecipeIngredient.objects.bulk_create(recipe_ingredients_to_create)

    return recipe.id

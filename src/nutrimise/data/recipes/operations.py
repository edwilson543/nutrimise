import attrs

from nutrimise.domain import embeddings, recipes

from . import models as recipe_models


@attrs.frozen
class RecipeAlreadyExists(Exception):
    name: str
    author_id: int | None

    def __str__(self) -> str:
        if self.author_id:
            return (
                f"Author {self.author_id} already has a recipe with name '{self.name}'"
            )
        else:
            return (
                f"Recipe with name '{self.name}' and anonymous author already exists."
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

    if recipe_models.Recipe.objects.filter(
        author_id=author_id, name__iexact=name
    ).exists():
        raise RecipeAlreadyExists(name=name, author_id=author_id)

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


def get_or_create_recipe_author(
    *, first_name: str, last_name: str
) -> recipes.RecipeAuthor:
    author, _ = recipe_models.RecipeAuthor.objects.get_or_create(
        first_name__iexact=first_name,
        last_name__iexact=last_name,
        defaults={"first_name": first_name, "last_name": last_name},
    )
    return author.to_domain_model()

import base64
import io

from django.db import transaction
from PIL import Image

from nutrimise.data.ingredients import operations as ingredient_operations
from nutrimise.data.ingredients import queries as ingredient_queries
from nutrimise.data.recipes import operations as recipe_operations
from nutrimise.domain import embeddings, image_extraction, ingredients, recipes

from . import _create_or_update_recipe_embedding


UnableToExtractRecipeFromImage = image_extraction.UnableToExtractRecipeFromImage
RecipeAlreadyExists = recipe_operations.RecipeAlreadyExists


def extract_recipe_from_image(
    *,
    author: recipes.RecipeAuthor | None,
    image: Image.Image,
    image_extraction_service: image_extraction.ImageExtractionService,
    embedding_service: embeddings.EmbeddingService,
) -> int:
    """
    Extract a recipe and its components from an image and save it to the database.

    :raises UnableToExtractRecipeFromImage: If the recipe could not be extracted for some reason.
    :raises RecipeAlreadyExists: If a recipe with the extracted name already exists for the
        author.
    """
    buffered = io.BytesIO()
    image.save(buffered, format=image.format)
    base64_image = base64.b64encode(buffered.getvalue())

    existing_ingredients = _get_existing_ingredients()

    extracted_recipe = image_extraction_service.extract_recipe_from_image(
        base64_image=base64_image.decode("utf-8"),
        existing_ingredients=existing_ingredients,
    )

    with transaction.atomic():
        ingredients_ = _get_or_create_ingredients(recipe=extracted_recipe)
        recipe_ingredients = [
            recipes.RecipeIngredient(
                ingredient=ingredients_[recipe_ingredient.ingredient.name],
                quantity=recipe_ingredient.quantity,
            )
            for recipe_ingredient in extracted_recipe.ingredients
        ]

        recipe_id = recipe_operations.create_recipe(
            author=author,
            name=extracted_recipe.name,
            description=extracted_recipe.description,
            methodology=extracted_recipe.methodology,
            number_of_servings=extracted_recipe.number_of_servings,
            meal_times=extracted_recipe.meal_times,
            recipe_ingredients=recipe_ingredients,
        )

    _create_or_update_recipe_embedding.create_or_update_recipe_embedding(
        recipe_id=recipe_id, embedding_service=embedding_service
    )

    return recipe_id


def _get_existing_ingredients() -> list[image_extraction.Ingredient]:
    ingredients_ = ingredient_queries.get_ingredients()
    return [
        image_extraction.Ingredient.from_domain_model(ingredient=ingredient)
        for ingredient in ingredients_
    ]


def _get_or_create_ingredients(
    *, recipe: image_extraction.Recipe
) -> dict[str, ingredients.Ingredient]:
    """
    Create any ingredients and categories extracted from the recipe that aren't in the database yet.

    :return: A mapping of ingredient names to `Ingredient` domain objects.
    """
    ingredient_categories: dict[str, ingredients.IngredientCategory] = {}
    ingredients_: dict[str, ingredients.Ingredient] = {}

    for recipe_ingredient in recipe.ingredients:
        category_name = recipe_ingredient.ingredient.category_name

        if category_name in ingredient_categories:
            category = ingredient_categories[category_name]
        else:
            category = ingredient_operations.get_or_create_ingredient_category(
                name=category_name
            )
            ingredient_categories[category_name] = category

        ingredient_name = recipe_ingredient.ingredient.name
        ingredient = ingredient_operations.get_or_create_ingredient(
            name=ingredient_name,
            category_id=category.id,
            units=recipe_ingredient.ingredient.units,
            grams_per_unit=recipe_ingredient.ingredient.grams_per_unit,
        )
        ingredients_[ingredient_name] = ingredient

    return ingredients_

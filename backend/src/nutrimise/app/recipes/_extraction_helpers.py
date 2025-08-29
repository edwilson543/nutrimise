from django.db import transaction

from nutrimise.data.ingredients import operations as ingredient_operations
from nutrimise.data.ingredients import queries as ingredient_queries
from nutrimise.data.recipes import operations as recipe_operations
from nutrimise.domain import data_extraction, ingredients, recipes


def get_existing_ingredients() -> list[data_extraction.Ingredient]:
    ingredients_ = ingredient_queries.get_ingredients()
    return [
        data_extraction.Ingredient.from_domain_model(ingredient=ingredient)
        for ingredient in ingredients_
    ]


def persist_extracted_recipe(
    extracted_recipe: data_extraction.Recipe, author: recipes.RecipeAuthor | None
) -> int:
    with transaction.atomic():
        ingredients_ = _get_or_create_ingredients(recipe=extracted_recipe)
        recipe_ingredients = [
            recipes.RecipeIngredient(
                ingredient=ingredients_[recipe_ingredient.ingredient.name],
                quantity=recipe_ingredient.quantity,
            )
            for recipe_ingredient in extracted_recipe.ingredients
        ]

        if not author and extracted_recipe.author:
            author = _get_or_create_recipe_author(author=extracted_recipe.author)

        return recipe_operations.create_recipe(
            author=author,
            name=extracted_recipe.name,
            description=extracted_recipe.description,
            methodology=extracted_recipe.methodology,
            number_of_servings=extracted_recipe.number_of_servings,
            meal_times=extracted_recipe.meal_times,
            recipe_ingredients=recipe_ingredients,
        )


def _get_or_create_recipe_author(
    *, author: data_extraction.RecipeAuthor
) -> recipes.RecipeAuthor:
    return recipe_operations.get_or_create_recipe_author(
        first_name=author.first_name,
        last_name=author.last_name,
    )


def _get_or_create_ingredients(
    *, recipe: data_extraction.Recipe
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

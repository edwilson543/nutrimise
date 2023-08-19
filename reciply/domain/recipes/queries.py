# Django imports
from django.contrib.auth import models as auth_models
from django.db import models as django_models

# Local application imports
from data.recipes import models as recipe_models
from domain import storage


def get_recipes_authored_by_user(
    author: auth_models.User,
) -> django_models.QuerySet[recipe_models.Recipe]:
    return recipe_models.Recipe.objects.filter(author=author)


def get_hero_image(recipe: recipe_models.Recipe) -> recipe_models.RecipeImage | None:
    try:
        return recipe.images.get(is_hero=True)
    except recipe_models.RecipeImage.DoesNotExist:
        return None


def get_image_source(recipe_image: recipe_models.RecipeImage) -> str:
    store = storage.get_file_storage()
    storage_context = store.context_class.from_recipe_image(recipe_image=recipe_image)
    try:
        return store.get_public_source(storage_context=storage_context)
    except storage.UnableToLocateFile:
        return ""

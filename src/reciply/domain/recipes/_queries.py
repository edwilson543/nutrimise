# Third party imports
import attrs

# Django imports
from django.contrib.auth import models as auth_models
from django.db import models as django_models

# Local application imports
from reciply.data.recipes import models as recipe_models
from reciply.domain import storage

from . import _model


@attrs.frozen
class RecipeDoesNotExist(Exception):
    recipe_id: int


def get_recipe(*, recipe_id: int) -> _model.Recipe:
    try:
        recipe = recipe_models.Recipe.objects.get(id=recipe_id)
    except recipe_models.Recipe.DoesNotExist as exc:
        raise RecipeDoesNotExist(recipe_id=recipe_id) from exc
    return _model.Recipe.from_orm_model(recipe=recipe)


def get_recipes() -> tuple[_model.Recipe, ...]:
    recipes = recipe_models.Recipe.objects.prefetch_related(
        "ingredients",
        "ingredients__ingredient",
        "ingredients__ingredient__nutritional_information",
    ).all()
    return tuple(_model.Recipe.from_orm_model(recipe=recipe) for recipe in recipes)


# Old queries.


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

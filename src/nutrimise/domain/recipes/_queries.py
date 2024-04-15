import attrs

from nutrimise.data.recipes import models as recipe_models

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

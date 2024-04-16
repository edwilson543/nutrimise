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


def get_recipes(
    *, dietary_requirement_ids: tuple[int, ...] = ()
) -> tuple[_model.Recipe, ...]:
    recipes = recipe_models.Recipe.objects.prefetch_related(
        "ingredients",
        "ingredients__ingredient",
        "ingredients__ingredient__nutritional_information",
    ).all()

    if dietary_requirement_ids:
        for dietary_requirement_id in dietary_requirement_ids:
            recipes = recipes.filter(
                ingredients__ingredient__dietary_requirements_satisfied=dietary_requirement_id
            )
    return tuple(_model.Recipe.from_orm_model(recipe=recipe) for recipe in recipes)

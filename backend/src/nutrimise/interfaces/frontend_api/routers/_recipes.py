from django.db import models as django_models
from fastapi import routing

from nutrimise.data.recipes import models as recipe_models
from nutrimise.data.recipes import operations as recipe_operations
from nutrimise.interfaces.frontend_api import auth, schemas


recipe_router = routing.APIRouter()


@recipe_router.get("/")
def list_recipes(user: auth.AuthenticatedUser) -> schemas.RecipeList:
    recipes = recipe_models.Recipe.objects.annotate(
        is_saved=django_models.Case(
            django_models.When(saves__user_id=user.id, then=True),
            default=False,
            output_field=django_models.BooleanField()
        )
    ).distinct().order_by("name")
    return schemas.RecipeList.from_orm(recipes)


@recipe_router.put("/{recipe_id}/save")
def save_recipe(recipe_id: int, user: auth.AuthenticatedUser) -> None:
    recipe_operations.save_recipe(recipe_id=recipe_id, user_id=user.id)


@recipe_router.put("/{recipe_id}/unsave")
def unsave_recipe(recipe_id: int, user: auth.AuthenticatedUser) -> None:
    recipe_operations.unsave_recipe(recipe_id=recipe_id, user_id=user.id)

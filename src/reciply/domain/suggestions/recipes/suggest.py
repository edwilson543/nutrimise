# Django imports
from django.contrib.auth import models as auth_models
from django.db import models as django_models

# Local application imports
from reciply.data.menus import models as menu_models
from reciply.data.recipes import models as recipe_models


def get_suggested_recipes_for_user(
    *, user: auth_models.User
) -> django_models.QuerySet[recipe_models.Recipe]:
    """
    get the suggested recipes for a user.
    """
    return recipe_models.Recipe.objects.filter(author=user).order_by("name")


def get_suggested_recipes_for_menu(
    *, menu: menu_models.Menu
) -> django_models.QuerySet[recipe_models.Recipe]:
    """
    Get the suggested recipes for a menu.
    """
    user = menu.author
    excluded_recipe_ids = [
        menu_item.recipe_id for menu_item in menu.items.all() if menu_item.recipe
    ]
    return (
        recipe_models.Recipe.objects.filter(author=user)
        .exclude(id__in=excluded_recipe_ids)
        .order_by("name")
    )

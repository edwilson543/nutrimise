# Django imports
from django import db as django_db
from django.db import transaction

# Local application imports
from data import constants
from data.menus import models as menu_models
from data.recipes import models as recipe_models


class RecipeDoesNotExist(django_db.IntegrityError):
    pass


@transaction.atomic
def add_item_to_menu(
    *,
    menu: menu_models.Menu,
    recipe_id: int,
    day: constants.Day,
    meal_time: constants.MealTime
) -> menu_models.MenuItem:
    recipe = recipe_models.Recipe.objects.get(id=recipe_id)
    try:
        menu_item = menu.items.get(meal_time=meal_time, day=day)
    except menu_models.MenuItem.DoesNotExist:
        return menu.add_item(recipe=recipe, day=day, meal_time=meal_time)
    if menu_item.recipe.id != recipe_id:
        menu_item.update_recipe(recipe)
    return menu_item

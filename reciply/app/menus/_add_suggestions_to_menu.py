# Local application imports
from data import constants
from data.menus import models as menu_models
from domain.suggestions.recipes import suggest as suggest_recipes

from . import _add_items_to_menu


def add_suggestions_to_menu(*, menu: menu_models.Menu) -> menu_models.Menu:
    # Add a suggestion for each day of the week to the menu
    n_days = 7
    suggestions = list(
        suggest_recipes.get_suggested_recipes_for_menu(menu=menu).values_list(
            "id", flat=True
        )
    )[:n_days]
    items_to_add: list[_add_items_to_menu.MenuItem] = []
    for n, recipe_id in enumerate(suggestions):
        day = constants.Day(n + 1)
        items_to_add.append(
            {
                "recipe_id": recipe_id,
                "day": day,
                "meal_time": constants.MealTime.DINNER,
            }
        )
    _add_items_to_menu.add_items_to_menu(menu=menu, items=items_to_add)
    return menu

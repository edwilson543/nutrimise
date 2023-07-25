# Third party imports
import pytest

# Local application imports
from app.menus import _add_items_to_menu
from data import constants
from tests import factories


class TestAddItemsToMenu:
    def test_add_single_item(self):
        menu = factories.Menu()

        recipe = factories.Recipe()
        item_to_add = {
            "recipe_id": recipe.id,
            "day": constants.Day.MONDAY,
            "meal_time": constants.MealTime.LUNCH,
        }

        _add_items_to_menu.add_items_to_menu(menu=menu, items=[item_to_add])

        menu_item = menu.items.get()
        assert menu_item.recipe == recipe
        assert menu_item.day == constants.Day.MONDAY
        assert menu_item.meal_time == constants.MealTime.LUNCH

    def test_adds_multiple_items(self):
        menu = factories.Menu()

        recipe = factories.Recipe()
        other_recipe = factories.Recipe()
        items_to_add = [
            {
                "recipe_id": recipe.id,
                "day": constants.Day.MONDAY,
                "meal_time": constants.MealTime.LUNCH,
            },
            {
                "recipe_id": other_recipe.id,
                "day": constants.Day.TUESDAY,
                "meal_time": constants.MealTime.DINNER,
            },
        ]

        _add_items_to_menu.add_items_to_menu(menu=menu, items=items_to_add)

        items = menu.items.order_by("day")
        monday_lunch = items.first()
        assert monday_lunch.recipe == recipe
        assert monday_lunch.day == constants.Day.MONDAY
        assert monday_lunch.meal_time == constants.MealTime.LUNCH
        tuesday_dinner = items.last()
        assert tuesday_dinner.recipe == other_recipe
        assert tuesday_dinner.day == constants.Day.TUESDAY
        assert tuesday_dinner.meal_time == constants.MealTime.DINNER

    def test_raises_when_adding_multiple_recipes_for_meal_time(self):
        menu = factories.Menu()

        recipe = factories.Recipe()
        other_recipe = factories.Recipe()
        items_to_add = [
            {
                "recipe_id": recipe.id,
                "day": constants.Day.MONDAY,
                "meal_time": constants.MealTime.LUNCH,
            },
            {
                "recipe_id": other_recipe.id,
                "day": constants.Day.MONDAY,
                "meal_time": constants.MealTime.LUNCH,
            },
        ]

        with pytest.raises(_add_items_to_menu.MealTimesAreNotUnique):
            _add_items_to_menu.add_items_to_menu(menu=menu, items=items_to_add)

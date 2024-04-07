# Third party imports
import pytest

# Local application imports
from reciply.app.menus import _add_item_to_menu
from reciply.data import constants
from reciply.data.recipes import models as recipe_models
from tests import factories


class TestAddItemToMenu:
    def test_create_menu_item_no_existing_items(self):
        menu = factories.Menu()
        recipe = factories.Recipe()

        _add_item_to_menu.add_item_to_menu(
            menu=menu,
            recipe_id=recipe.id,
            day=constants.Day.MONDAY,
            meal_time=constants.MealTime.LUNCH,
        )

        menu_item = menu.items.get()
        assert menu_item.recipe == recipe
        assert menu_item.day == constants.Day.MONDAY
        assert menu_item.meal_time == constants.MealTime.LUNCH

    def test_updates_existing_menu_item_at_day_and_meal_time(self):
        menu = factories.Menu()
        menu_item = factories.MenuItem(
            menu=menu, day=constants.Day.MONDAY, meal_time=constants.MealTime.LUNCH
        )
        recipe = factories.Recipe()

        _add_item_to_menu.add_item_to_menu(
            menu=menu_item.menu,
            recipe_id=recipe.id,
            day=menu_item.day,
            meal_time=menu_item.meal_time,
        )

        updated_menu_item = menu.items.get()
        assert updated_menu_item.id == menu_item.id
        assert updated_menu_item.recipe == recipe
        assert updated_menu_item.day == constants.Day.MONDAY
        assert updated_menu_item.meal_time == constants.MealTime.LUNCH

    def test_raises_does_not_exist_if_recipe_id_is_invalid(self):
        menu = factories.Menu()

        with pytest.raises(recipe_models.Recipe.DoesNotExist):
            _add_item_to_menu.add_item_to_menu(
                menu=menu,
                recipe_id=1000000000,
                day=constants.Day.MONDAY,
                meal_time=constants.MealTime.LUNCH,
            )

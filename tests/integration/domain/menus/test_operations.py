from nutrimise.domain import menus
from tests.factories import data as data_factories


class TestUpdateMenuItemRecipe:
    def test_updates_menu_item_recipe(self):
        recipe = data_factories.Recipe()
        menu_item = data_factories.MenuItem(recipe_id=None)

        menus.update_menu_item_recipe(menu_item_id=menu_item.id, recipe_id=recipe.id)

        menu_item.refresh_from_db()
        assert menu_item.recipe == recipe

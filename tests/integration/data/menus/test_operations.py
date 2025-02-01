from nutrimise.data.menus import operations
from tests.factories import data as data_factories


class TestUpdateMenuItemRecipe:
    def test_updates_menu_item_recipe(self):
        recipe = data_factories.Recipe()
        menu_item = data_factories.MenuItem(recipe_id=None)

        operations.update_menu_item_recipe(
            menu_item_id=menu_item.id, recipe_id=recipe.id
        )

        menu_item.refresh_from_db()
        assert menu_item.recipe == recipe

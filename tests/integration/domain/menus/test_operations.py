# Local application imports
from reciply.domain import menus
from tests import factories


class TestUpdateMenuItemRecipe:
    def test_updates_menu_item_recipe(self):
        recipe = factories.Recipe()
        menu_item = factories.MenuItem(recipe_id=None)

        menus.update_menu_item_recipe(menu_item_id=menu_item.id, recipe_id=recipe.id)

        menu_item.refresh_from_db()
        assert menu_item.recipe == recipe

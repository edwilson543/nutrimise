# Local application imports
from reciply.data.menus import models as menu_models


def update_menu_item_recipe(*, menu_item_id: int, recipe_id: int) -> None:
    menu_item = menu_models.MenuItem.objects.get(id=menu_item_id)
    menu_item.update_recipe(recipe_id=recipe_id)

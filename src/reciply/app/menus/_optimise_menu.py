# Third party imports
import attrs

# Local application imports
from reciply.domain import menus, recipes

MenuDoesNotExist = menus.MenuDoesNotExist


@attrs.frozen
class OptimiserDidNotDoItsJob(Exception):
    menu_item_ids: list[int]


def optimise_menu(*, menu_id: int) -> None:
    menu = menus.get_menu(menu_id=menu_id)
    recipes_to_consider = recipes.get_recipes()

    optimised_menu = menus.optimise_recipes_for_menu(
        menu=menu, recipes_to_consider=recipes_to_consider
    )

    for menu_item in optimised_menu.items:
        # For mypy. The solver will raise if a menu item couldn't be solved.
        assert menu_item.recipe_id
        if menu_item.optimiser_generated:
            menus.update_menu_item_recipe(
                menu_item_id=menu_item.id, recipe_id=menu_item.recipe_id
            )

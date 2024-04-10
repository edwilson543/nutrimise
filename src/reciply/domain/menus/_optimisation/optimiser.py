from __future__ import annotations

# Local application imports
from reciply.domain import menus, recipes


def optimise_recipes_for_menu(
    *,
    menu: menus.Menu,
    recipes_to_consider: tuple[recipes.Recipe, ...],
    # TODO -> will need to match by ID.
) -> menus.Menu:
    # Create problem.
    # Generate decision variables (without making any queries).
    # Add constraints.
    # Add objective.
    # Solve.
    return menu


class DecisionVariable:
    def __init__(self, *, recipe: recipes.Recipe, menu_item: menus.MenuItem):
        self.recipe = recipe
        self.menu_item = menu_item
        # TODO -> set LP variable.

    def __str__(self) -> str:
        return f"recipe_{self.recipe.id}_at_menu_item_{self.menu_item.id}"

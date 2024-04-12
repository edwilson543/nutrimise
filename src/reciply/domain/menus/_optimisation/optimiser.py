from __future__ import annotations

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

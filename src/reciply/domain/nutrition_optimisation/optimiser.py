from __future__ import annotations

# Standard library imports
import dataclasses

# Local application imports
from reciply.data import constants
from reciply.data.menus import models as menu_models
from reciply.domain import menus, recipes


@dataclasses.dataclass(frozen=True)
class MenuRequirements:
    daily_nutrient_requirements: list[NutrientRequirement]
    maximum_occurrences_per_recipe: dict[constants.MealTime, int]


@dataclasses.dataclass(frozen=True)
class NutrientRequirement:
    nutrient_id: int
    minimum_grams: float | None
    maximum_grams: float | None
    target_grams: float | None


def optimise_recipes_for_menu(
    *,
    menu: menus.Menu,
    requirements: MenuRequirements,
    recipe_to_consider: list[recipes.Recipe],
    # TODO -> will need to match by ID.
) -> menu_models.Menu:
    pass
    # Create problem.
    # Generate decision variables (without making any queries).
    # Add constraints.
    # Add objective.
    # Solve.


class DecisionVariable:
    def __init__(self, *, recipe: recipes.Recipe, menu_item: menus.MenuItem):
        self.recipe = recipe
        self.menu_item = menu_item
        # TODO -> set LP variable.

    def __str__(self) -> str:
        return f"recipe_{self.recipe.id}_at_menu_item_{self.menu_item.id}"

from __future__ import annotations

import attrs
import pulp as lp

from reciply.data import constants
from reciply.domain import menus, recipes

from . import inputs


class DecisionVariable:
    def __init__(self, *, recipe: recipes.Recipe, menu_item: menus.MenuItem) -> None:
        self.recipe = recipe
        self.menu_item = menu_item

        self.lp_variable = lp.LpVariable(
            cat=lp.constants.LpBinary,
            name=f"recipe-{recipe.id}-for-menu-item-{menu_item.id}",
        )

    @property
    def day(self) -> constants.Day:
        return self.menu_item.day


@attrs.frozen
class Variables:
    decision_variables: tuple[DecisionVariable, ...]

    @classmethod
    def from_inputs(cls, inputs: inputs.OptimiserInputs) -> Variables:
        decision_variables: list[DecisionVariable] = []

        for menu_item in inputs.menu.items:
            if not menu_item.optimiser_generated:
                # This menu item is already solved.
                continue

            for recipe in inputs.recipes_to_consider:
                # Only create a variable if the recipe is for the given meal time.
                if menu_item.meal_time in recipe.meal_times:
                    decision_variable = DecisionVariable(
                        recipe=recipe, menu_item=menu_item
                    )
                    decision_variables.append(decision_variable)

        return cls(decision_variables=tuple(decision_variables))

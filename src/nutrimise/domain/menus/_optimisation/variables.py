from __future__ import annotations

import attrs
import pulp as lp

from nutrimise.data import constants
from nutrimise.domain import ingredients, menus, recipes

from . import inputs


class DecisionVariable:
    def __init__(self, *, recipe: recipes.Recipe, menu_item: menus.MenuItem) -> None:
        self.recipe = recipe
        self.menu_item = menu_item

        self.lp_variable = lp.LpVariable(
            cat=lp.constants.LpBinary,
            name=f"recipe_{recipe.id}_for_menu_item_{menu_item.id}",
        )

    @property
    def day(self) -> constants.Day:
        return self.menu_item.day


class IngredientIncludedDependentVariable:
    def __init__(self, *, ingredient: ingredients.Ingredient) -> None:
        self.ingredient = ingredient
        self.lp_variable = lp.LpVariable(
            cat=lp.constants.LpBinary,
            name=f"ingredient_{ingredient.id}_included_in_menu",
        )


@attrs.frozen
class Variables:
    decision_variables: tuple[DecisionVariable, ...]
    # Dependent variables.
    ingredient_included_dependent_variables: tuple[
        IngredientIncludedDependentVariable, ...
    ]

    @classmethod
    def from_inputs(cls, inputs: inputs.OptimiserInputs) -> Variables:
        return cls(
            decision_variables=cls._decision_variables_from_inputs(inputs),
            ingredient_included_dependent_variables=cls._ingredient_included_variables_from_inputs(
                inputs
            ),
        )

    @classmethod
    def _decision_variables_from_inputs(
        cls, inputs: inputs.OptimiserInputs
    ) -> tuple[DecisionVariable, ...]:
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
        return tuple(decision_variables)

    @classmethod
    def _ingredient_included_variables_from_inputs(
        cls, inputs: inputs.OptimiserInputs
    ) -> tuple[IngredientIncludedDependentVariable, ...]:
        return tuple(
            IngredientIncludedDependentVariable(ingredient=ingredient)
            for ingredient in inputs.relevant_ingredients
            if ingredient not in inputs.unoptimised_ingredient_selections
        )

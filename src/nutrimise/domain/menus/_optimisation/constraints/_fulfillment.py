from typing import Generator

import pulp as lp

from .. import expressions, inputs, variables


def all_menu_items_are_assigned_a_recipe(
    *, inputs: inputs.OptimiserInputs, variables_: variables.Variables
) -> Generator[lp.LpConstraint, None, None]:
    for menu_item in inputs.menu.items:
        if not menu_item.optimiser_generated:
            continue
        sum_of_menu_item_variables = expressions.sum_all_variables_for_menu_item(
            variables_=variables_, menu_item_id=menu_item.id
        )
        yield sum_of_menu_item_variables == 1


def recipes_do_not_exceed_maximum_occurrences(
    *,
    inputs: inputs.OptimiserInputs,
    variables_: variables.Variables,
) -> lp.LpAffineExpression:
    for recipe in inputs.recipes_to_consider:
        number_of_occurrences_of_recipe = expressions.number_of_occurrences_of_recipe(
            inputs=inputs, variables_=variables_, recipe_id=recipe.id
        )
        yield (
            number_of_occurrences_of_recipe
            <= inputs.requirements.maximum_occurrences_per_recipe
        )

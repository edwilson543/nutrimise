from typing import Generator

import pulp as lp

from .. import inputs, variables
from . import _fulfillment, _nutrient, _variety


def yield_all_constraints(
    *,
    inputs: inputs.OptimiserInputs,
    variables_: variables.Variables,
) -> Generator[lp.LpConstraint, None, None]:
    yield from _fulfillment.all_menu_items_are_assigned_a_recipe(
        inputs=inputs, variables_=variables_
    )
    yield from _fulfillment.recipes_do_not_exceed_maximum_occurrences(
        inputs=inputs, variables_=variables_
    )
    if inputs.requirements.nutrient_requirements:
        yield from _nutrient.all_nutrient_requirements_are_met(
            inputs=inputs, variables_=variables_
        )
    if inputs.requirements.variety_requirements:
        yield from _variety.all_variety_requirements_are_met(
            inputs=inputs, variables=variables_
        )

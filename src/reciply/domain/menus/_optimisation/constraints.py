from typing import Generator

import attrs
import pulp as lp

from reciply.data import constants
from reciply.domain import menus

from . import expressions, inputs, variables


@attrs.frozen
class EnforcementIntervalNotImplemented(Exception):
    interval: constants.NutrientRequirementEnforcementInterval


def yield_all_constraints(
    *,
    inputs: inputs.OptimiserInputs,
    variables_: variables.Variables,
) -> Generator[lp.LpConstraint, None, None]:
    yield from _all_menu_items_assigned_a_recipe(inputs=inputs, variables_=variables_)
    yield from _maximum_occurrences_per_recipe(inputs=inputs, variables_=variables_)
    yield from _nutrient_requirements(inputs=inputs, variables_=variables_)


def _all_menu_items_assigned_a_recipe(
    *, inputs: inputs.OptimiserInputs, variables_: variables.Variables
) -> Generator[lp.LpConstraint, None, None]:
    for menu_item in inputs.menu.items:
        if not menu_item.optimiser_generated:
            continue
        sum_of_menu_item_variables = expressions.sum_all_variables_for_menu_item(
            variables_=variables_, menu_item_id=menu_item.id
        )
        yield sum_of_menu_item_variables == 1


def _maximum_occurrences_per_recipe(
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


def _nutrient_requirements(
    *, inputs: inputs.OptimiserInputs, variables_: variables.Variables
) -> Generator[lp.LpConstraint, None, None]:
    for nutrient_requirement in inputs.requirements.nutrient_requirements:
        match nutrient_requirement.enforcement_interval:
            case constants.NutrientRequirementEnforcementInterval.DAILY:
                yield from _daily_nutrient_requirements(
                    inputs=inputs,
                    requirement=nutrient_requirement,
                    variables_=variables_,
                )
            case _:
                raise EnforcementIntervalNotImplemented(
                    interval=nutrient_requirement.enforcement_interval
                )


def _daily_nutrient_requirements(
    *,
    inputs: inputs.OptimiserInputs,
    variables_: variables.Variables,
    requirement: menus.NutrientRequirement,
) -> Generator[lp.LpConstraint, None, None]:
    for day in inputs.menu.days:
        # TODO: ensure units are consistent.
        total_nutrient_quantity_for_day = expressions.total_nutrient_quantity_for_day(
            inputs=inputs,
            variables=variables_,
            day=day,
            nutrient_id=requirement.nutrient_id,
        )
        if requirement.minimum_quantity is not None:
            yield total_nutrient_quantity_for_day >= requirement.minimum_quantity
        if requirement.maximum_quantity is not None:
            yield total_nutrient_quantity_for_day <= requirement.maximum_quantity

from typing import Generator

import attrs
import pulp as lp

from nutrimise.data import constants
from nutrimise.domain import menus

from .. import expressions, inputs, variables


@attrs.frozen
class EnforcementIntervalNotImplemented(Exception):
    interval: constants.NutrientRequirementEnforcementInterval


def all_nutrient_requirements_are_met(
    *, inputs: inputs.OptimiserInputs, variables_: variables.Variables
) -> Generator[lp.LpConstraint, None, None]:
    for nutrient_requirement in inputs.requirements.nutrient_requirements:
        match nutrient_requirement.enforcement_interval:
            case constants.NutrientRequirementEnforcementInterval.DAILY:
                yield from _daily_nutrient_requirements_are_met(
                    inputs=inputs,
                    requirement=nutrient_requirement,
                    variables_=variables_,
                )
            case _:
                raise EnforcementIntervalNotImplemented(
                    interval=nutrient_requirement.enforcement_interval
                )


def _daily_nutrient_requirements_are_met(
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

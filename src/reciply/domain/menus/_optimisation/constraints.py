from typing import Generator

import attrs
import pulp as lp

from reciply.data.menus import models as menu_models
from reciply.domain import menus

from . import expressions, variables


@attrs.frozen
class EnforcementIntervalNotImplemented(Exception):
    interval: menu_models.NutrientRequirementEnforcementInterval


def yield_all_constraints(
    *, menu: menus.Menu, variables_: variables.Variables
) -> Generator[lp.LpConstraint, None, None]:
    yield from _nutrient_requirements(menu=menu, variables_=variables_)


def _nutrient_requirements(
    *, menu: menus.Menu, variables_: variables.Variables
) -> Generator[lp.LpConstraint, None, None]:
    assert menu.requirements  # Solver will not be given menu without requirements.
    for nutrient_requirement in menu.requirements.nutrient_requirements:
        match nutrient_requirement.enforcement_interval:
            case menu_models.NutrientRequirementEnforcementInterval.DAILY:
                yield from _daily_nutrient_requirements(
                    requirement=nutrient_requirement, variables_=variables_, menu=menu
                )
            case _:
                raise EnforcementIntervalNotImplemented(
                    interval=nutrient_requirement.enforcement_interval
                )


def _daily_nutrient_requirements(
    *,
    requirement: menus.NutrientRequirement,
    variables_: variables.Variables,
    menu: menus.Menu,
) -> Generator[lp.LpConstraint, None, None]:
    for day in menu.days:
        total_nutrient_grams_for_day = expressions.total_nutrient_grams_for_day(
            variables_=variables_, day=day, nutrient_id=requirement.nutrient_id
        )
        if requirement.minimum_grams is not None:
            yield total_nutrient_grams_for_day >= requirement.minimum_grams
        if requirement.maximum_grams is not None:
            yield total_nutrient_grams_for_day <= requirement.maximum_grams

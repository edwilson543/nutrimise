from typing import Generator

import attrs
import pulp as lp

from reciply.data.menus import models as menu_models
from reciply.domain import menus, recipes

from . import expressions, variables


@attrs.frozen
class EnforcementIntervalNotImplemented(Exception):
    interval: menu_models.NutrientRequirementEnforcementInterval


def yield_all_constraints(
    *,
    menu: menus.Menu,
    recipes_: tuple[recipes.Recipe, ...],
    variables_: variables.Variables,
) -> Generator[lp.LpConstraint, None, None]:
    yield from _all_menu_items_assigned_a_recipe(menu=menu, variables_=variables_)
    yield from _maximum_occurrences_per_recipe(
        recipes_=recipes_, menu=menu, variables_=variables_
    )
    yield from _nutrient_requirements(menu=menu, variables_=variables_)


def _all_menu_items_assigned_a_recipe(
    *, menu: menus.Menu, variables_: variables.Variables
) -> Generator[lp.LpConstraint, None, None]:
    for menu_item in menu.items:
        if not menu_item.optimiser_generated:
            continue
        sum_of_menu_item_variables = expressions.sum_all_variables_for_menu_item(
            variables_=variables_, menu_item_id=menu_item.id
        )
        yield sum_of_menu_item_variables == 1


def _maximum_occurrences_per_recipe(
    *,
    recipes_: tuple[recipes.Recipe, ...],
    menu: menus.Menu,
    variables_: variables.Variables,
) -> lp.LpAffineExpression:
    for recipe in recipes_:
        sum_of_all_recipe_variables = expressions.sum_all_variables_for_recipe(
            variables_=variables_, recipe_id=recipe.id
        )
        yield (
            sum_of_all_recipe_variables
            <= menu.requirements.maximum_occurrences_per_recipe
        )


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

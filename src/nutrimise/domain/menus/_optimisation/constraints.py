from typing import Generator

import attrs
import pulp as lp

from nutrimise.data import constants
from nutrimise.domain import menus

from . import expressions, inputs, variables


@attrs.frozen
class EnforcementIntervalNotImplemented(Exception):
    interval: constants.NutrientRequirementEnforcementInterval


def yield_all_constraints(
    *,
    inputs: inputs.OptimiserInputs,
    variables_: variables.Variables,
) -> Generator[lp.LpConstraint, None, None]:
    yield from _all_menu_items_are_assigned_a_recipe(
        inputs=inputs, variables_=variables_
    )
    yield from _recipes_do_not_exceed_maximum_occurrences(
        inputs=inputs, variables_=variables_
    )
    if inputs.requirements.nutrient_requirements:
        yield from _all_nutrient_requirements_are_met(
            inputs=inputs, variables_=variables_
        )
    if inputs.requirements.variety_requirements:
        yield from _all_variety_requirements_are_met(
            inputs=inputs, variables=variables_
        )


# Fulfillment.


def _all_menu_items_are_assigned_a_recipe(
    *, inputs: inputs.OptimiserInputs, variables_: variables.Variables
) -> Generator[lp.LpConstraint, None, None]:
    for menu_item in inputs.menu.items:
        if not menu_item.optimiser_generated:
            continue
        sum_of_menu_item_variables = expressions.sum_all_variables_for_menu_item(
            variables_=variables_, menu_item_id=menu_item.id
        )
        yield sum_of_menu_item_variables == 1


def _recipes_do_not_exceed_maximum_occurrences(
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


# Nutrition.


def _all_nutrient_requirements_are_met(
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


# Variety.


def _all_variety_requirements_are_met(
    *, inputs: inputs.OptimiserInputs, variables: variables.Variables
) -> Generator[lp.LpConstraint, None, None]:
    yield from _ingredient_included_if_a_recipe_it_features_in_is_included(
        variables=variables
    )
    yield from _ingredient_excluded_if_no_recipe_it_features_in_is_included(
        variables=variables
    )
    for variety_requirement in inputs.requirements.variety_requirements:
        yield from _variety_requirement_met_for_ingredient_category(
            inputs=inputs, variables=variables, requirement=variety_requirement
        )


def _ingredient_included_if_a_recipe_it_features_in_is_included(
    *,
    variables: variables.Variables,
) -> Generator[lp.LpConstraint, None, None]:
    for ingredient_inclusion_var in variables.ingredient_included_dependent_variables:
        for decision_variable in variables.decision_variables:
            if (
                ingredient_inclusion_var.ingredient.id
                in decision_variable.recipe.unique_ingredient_ids
            ):
                yield (
                    ingredient_inclusion_var.lp_variable
                    >= decision_variable.lp_variable
                )


def _ingredient_excluded_if_no_recipe_it_features_in_is_included(
    *,
    variables: variables.Variables,
) -> Generator[lp.LpConstraint, None, None]:
    for ingredient_inclusion_var in variables.ingredient_included_dependent_variables:
        number_of_times_ingredient_features_across_menu = (
            expressions.number_of_times_ingredient_features_across_menu(
                variables=variables,
                ingredient_id=ingredient_inclusion_var.ingredient.id,
            )
        )
        yield (
            ingredient_inclusion_var.lp_variable
            <= number_of_times_ingredient_features_across_menu
        )


def _variety_requirement_met_for_ingredient_category(
    *,
    inputs: inputs.OptimiserInputs,
    variables: variables.Variables,
    requirement: menus.VarietyRequirement,
) -> Generator[lp.LpConstraint, None, None]:
    number_of_ingredients = expressions.number_of_ingredients_in_category_across_menu(
        inputs=inputs,
        variables=variables,
        ingedient_category_id=requirement.ingredient_category_id,
    )
    if requirement.minimum:
        yield number_of_ingredients >= requirement.minimum
    if requirement.maximum:
        yield number_of_ingredients <= requirement.maximum

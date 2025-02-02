from typing import Generator

import pulp as lp

from nutrimise.domain import menus
from nutrimise.domain.optimisation import _expressions, _inputs, _variables


def all_variety_requirements_are_met(
    *, inputs: _inputs.OptimiserInputs, variables: _variables.Variables
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
    variables: _variables.Variables,
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
    variables: _variables.Variables,
) -> Generator[lp.LpConstraint, None, None]:
    for ingredient_inclusion_var in variables.ingredient_included_dependent_variables:
        number_of_times_ingredient_features_across_menu = (
            _expressions.number_of_times_ingredient_features_across_menu(
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
    inputs: _inputs.OptimiserInputs,
    variables: _variables.Variables,
    requirement: menus.VarietyRequirement,
) -> Generator[lp.LpConstraint, None, None]:
    number_of_ingredients = _expressions.number_of_ingredients_in_category_across_menu(
        inputs=inputs,
        variables=variables,
        ingredient_category_id=requirement.ingredient_category_id,
    )
    if requirement.minimum is not None:
        yield number_of_ingredients >= requirement.minimum
    if requirement.maximum is not None:
        yield number_of_ingredients <= requirement.maximum

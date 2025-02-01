from typing import Generator

import attrs
import pulp as lp

from nutrimise.domain import menus
from nutrimise.domain.optimisation import _expressions, _inputs, _variables


@attrs.frozen
class NoVarietyTargetsSet(Exception):
    menu_id: int

    def __str__(self) -> str:
        return (
            "Menu optimisation mode is set to 'Ingredient variety' but no variety targets are set. "
            "Either change the optimisation mode, or set at least one variety target."
        )


class _VarietyObjectiveVariable:
    """
    Dependent variable bounding the deviation from a variety target.
    """

    def __init__(self, *, requirement: menus.VarietyRequirement) -> None:
        self.requirement = requirement

        self.lp_variable = lp.LpVariable(
            name=f"ingredient-category-{requirement.ingredient_category_id}-target-deviation",
            cat=lp.LpInteger,
        )

    @property
    def category_id(self) -> int:
        return self.requirement.ingredient_category_id


def add_variety_objective_to_problem(
    *,
    problem: lp.LpProblem,
    inputs: _inputs.OptimiserInputs,
    variables: _variables.Variables,
) -> lp.LpProblem:
    """
    Add an objective to the problem that forces the solution towards the variety targets.
    """
    variety_objective_variables = _get_variety_objective_variables(inputs=inputs)
    if len(variety_objective_variables) == 0:
        raise NoVarietyTargetsSet(menu_id=inputs.menu.id)

    for constraint in _yield_all_variety_objective_constraints(
        inputs=inputs,
        variables=variables,
        variety_objective_variables=variety_objective_variables,
    ):
        problem += constraint

    objective = _get_variety_objective(
        variety_objective_variables=variety_objective_variables
    )
    problem += objective

    return problem


def _get_variety_objective(
    variety_objective_variables: tuple[_VarietyObjectiveVariable, ...],
) -> lp.LpAffineExpression:
    """
    Get a normalized sum of the deviation from the variety targets.

    The sum is normalized to support objectives that combine multiple metrics.
    """
    total_deviation = lp.lpSum(
        variable.lp_variable for variable in variety_objective_variables
    )
    return total_deviation / len(variety_objective_variables)


def _yield_all_variety_objective_constraints(
    *,
    inputs: _inputs.OptimiserInputs,
    variables: _variables.Variables,
    variety_objective_variables: tuple[_VarietyObjectiveVariable, ...],
) -> Generator[lp.LpConstraint, None, None]:
    """
    Big M constraints on the objective's deviation from each variety target.
    """
    for variable in variety_objective_variables:
        number_of_ingredients = (
            _expressions.number_of_ingredients_in_category_across_menu(
                inputs=inputs,
                variables=variables,
                ingredient_category_id=variable.category_id,
            )
        )
        yield (
            variable.lp_variable >= number_of_ingredients - variable.requirement.target
        )
        yield (
            variable.lp_variable >= -number_of_ingredients + variable.requirement.target
        )


def _get_variety_objective_variables(
    *, inputs: _inputs.OptimiserInputs
) -> tuple[_VarietyObjectiveVariable, ...]:
    variables = [
        _VarietyObjectiveVariable(requirement=requirement)
        for requirement in inputs.requirements.variety_requirements
        if requirement.target is not None
    ]
    return tuple(variables)

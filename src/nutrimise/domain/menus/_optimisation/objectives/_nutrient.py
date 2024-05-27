from typing import Generator

import attrs
import pulp as lp

from nutrimise.domain import menus

from .. import expressions, inputs, variables


@attrs.frozen
class NoNutrientTargetsSet(Exception):
    menu_id: int


class _NutrientObjectiveVariable:
    """
    Dependent variable bounding the deviation from a nutrient target on a given day.
    """

    def __init__(self, *, requirement: menus.NutrientRequirement, day: int) -> None:
        self.requirement = requirement
        self.day = day

        self.lp_variable = lp.LpVariable(
            name=f"nutrient-{requirement.nutrient_id}-target-deviation",
            cat=lp.LpContinuous,
        )

    @property
    def nutrient_id(self) -> int:
        return self.requirement.nutrient_id


def add_nutrient_objective_to_problem(
    *,
    problem: lp.LpProblem,
    inputs: inputs.OptimiserInputs,
    variables: variables.Variables,
) -> lp.LpProblem:
    """
    Add an objective to the problem that forces the solution towards the nutrient targets.
    """
    nutrient_objective_variables = _get_nutrient_objective_variables(inputs=inputs)
    if len(nutrient_objective_variables) == 0:
        raise NoNutrientTargetsSet(menu_id=inputs.menu.id)

    for constraint in _yield_all_nutrient_objective_constraints(
        inputs=inputs,
        variables=variables,
        nutrient_objective_variables=nutrient_objective_variables,
    ):
        problem += constraint

    objective = _get_nutrient_objective(
        nutrient_objective_variables=nutrient_objective_variables
    )
    problem += objective

    return problem


def _get_nutrient_objective(
    nutrient_objective_variables: tuple[_NutrientObjectiveVariable, ...],
) -> lp.LpAffineExpression:
    """
    Get a normalized sum of the deviation from the nutrient targets.

    The sum is normalized to support objectives that combine multiple metrics.
    """
    total_deviation = lp.lpSum(
        variable.lp_variable for variable in nutrient_objective_variables
    )
    return total_deviation / len(nutrient_objective_variables)


def _yield_all_nutrient_objective_constraints(
    *,
    inputs: inputs.OptimiserInputs,
    variables: variables.Variables,
    nutrient_objective_variables: tuple[_NutrientObjectiveVariable, ...],
) -> Generator[lp.LpConstraint, None, None]:
    """
    Big M constraints on the objective's deviation from each nutrient target.
    """
    for variable in nutrient_objective_variables:
        total_nutrient_quantity = expressions.total_nutrient_quantity_for_day(
            inputs=inputs,
            variables=variables,
            day=variable.day,
            nutrient_id=variable.nutrient_id,
        )
        yield (
            variable.lp_variable
            >= total_nutrient_quantity - variable.requirement.target_quantity
        )
        yield (
            variable.lp_variable
            >= -total_nutrient_quantity + variable.requirement.target_quantity
        )


def _get_nutrient_objective_variables(
    *, inputs: inputs.OptimiserInputs
) -> tuple[_NutrientObjectiveVariable, ...]:
    variables = [
        _NutrientObjectiveVariable(requirement=requirement, day=day)
        for requirement in inputs.requirements.nutrient_requirements
        if requirement.target_quantity is not None
        for day in inputs.menu.days
    ]
    return tuple(variables)

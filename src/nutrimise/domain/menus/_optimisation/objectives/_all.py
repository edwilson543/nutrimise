import attrs
import pulp as lp

from nutrimise.data import constants

from .. import inputs, variables
from . import _nutrient, _random, _variety


@attrs.frozen
class NoTargetsSet(Exception):
    menu_id: int

    def __str__(self) -> str:
        return (
            "Menu optimisation mode is set to 'Everything' but no targets are set. "
            "Either change the optimisation mode, or set at least one target."
        )


def add_objective_to_problem(
    *,
    problem: lp.LpProblem,
    inputs: inputs.OptimiserInputs,
    variables: variables.Variables,
) -> lp.LpProblem:
    """
    Return the LP problem with the objectives function(s) installed.
    """
    match inputs.requirements.optimisation_mode:
        case constants.OptimisationMode.RANDOM:
            return _random.add_random_objective_to_problem(
                problem=problem, variables=variables
            )
        case constants.OptimisationMode.NUTRIENT:
            return _nutrient.add_nutrient_objective_to_problem(
                problem=problem, inputs=inputs, variables=variables
            )
        case constants.OptimisationMode.VARIETY:
            return _variety.add_variety_objective_to_problem(
                problem=problem, inputs=inputs, variables=variables
            )
        case constants.OptimisationMode.EVERYTHING:
            return _add_everything_objective_to_problem(
                problem=problem, inputs=inputs, variables=variables
            )


def _add_everything_objective_to_problem(
    *,
    problem: lp.LpProblem,
    inputs: inputs.OptimiserInputs,
    variables: variables.Variables,
) -> lp.LpProblem:
    """
    Return the objective to use when optimising for 'everything'.
    """
    no_objectives_added = True

    try:
        problem = _nutrient.add_nutrient_objective_to_problem(
            problem=problem, inputs=inputs, variables=variables
        )
        no_objectives_added = False
    except _nutrient.NoNutrientTargetsSet:
        pass

    try:
        problem = _variety.add_variety_objective_to_problem(
            problem=problem, inputs=inputs, variables=variables
        )
        no_objectives_added = False
    except _variety.NoVarietyTargetsSet:
        pass

    if no_objectives_added:
        raise NoTargetsSet(menu_id=inputs.menu.id)

    return problem

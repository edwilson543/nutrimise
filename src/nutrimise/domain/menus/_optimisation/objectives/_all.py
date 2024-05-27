import attrs
import pulp as lp

from nutrimise.data import constants

from .. import inputs, variables
from . import _nutrient, _random


@attrs.frozen
class NoTargetsSet(Exception):
    menu_id: int


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
    n_objectives_added = 0

    try:
        problem = _nutrient.add_nutrient_objective_to_problem(
            problem=problem, inputs=inputs, variables=variables
        )
        n_objectives_added += 1
    except _nutrient.NoNutrientTargetsSet:
        pass

    if n_objectives_added == 0:
        raise NoTargetsSet(menu_id=inputs.menu.id)

    return problem

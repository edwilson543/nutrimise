import pulp as lp

from nutrimise.data import constants

from .. import inputs, variables
from . import _nutrient, _random


def add_objective_to_problem(
    *,
    problem: lp.LpProblem,
    inputs: inputs.OptimiserInputs,
    variables: variables.Variables,
) -> lp.LpProblem:
    """
    Return the LP problem with the objective function installed.
    """
    match inputs.requirements.optimisation_mode:
        case constants.OptimisationMode.RANDOM:
            return _random.add_random_objective_to_problem(
                problem=problem, variables=variables
            )
        case constants.OptimisationMode.NUTRIENT:
            return _nutrient.add_nutrient_objective_to_problem(
                problem=problem, inputs=inputs, decision_variables=variables
            )

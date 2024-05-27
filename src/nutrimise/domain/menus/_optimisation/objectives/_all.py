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
    Return the LP problem with the objectives function(s) installed.
    """
    mode = inputs.requirements.optimisation_mode

    if mode == constants.OptimisationMode.RANDOM:
        problem = _random.add_random_objective_to_problem(
            problem=problem, variables=variables
        )
    if mode in [
        constants.OptimisationMode.NUTRIENT,
        constants.OptimisationMode.EVERYTHING,
    ]:
        problem = _nutrient.add_nutrient_objective_to_problem(
            problem=problem, inputs=inputs, decision_variables=variables
        )
    return problem

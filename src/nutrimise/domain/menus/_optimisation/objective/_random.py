import random

import pulp as lp

from .. import variables


def add_random_objective_to_problem(
    *, problem: lp.LpProblem, variables: variables.Variables
) -> lp.LpProblem:
    """
    Ensure the solution is random, while satisfying the requirements.
    """
    objective_function = lp.lpSum(
        random.random() * variable.lp_variable
        for variable in variables.decision_variables
    )
    problem += objective_function
    problem.sense = lp.LpMinimize
    return problem

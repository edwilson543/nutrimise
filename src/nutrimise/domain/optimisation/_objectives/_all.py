import attrs
import pulp as lp

from nutrimise.domain import menus
from nutrimise.domain.optimisation import _inputs, _variables

from . import _nutrient, _random, _semantic, _variety


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
    inputs: _inputs.OptimiserInputs,
    variables: _variables.Variables,
) -> lp.LpProblem:
    """
    Return the LP problem with the objectives function(s) installed.
    """
    match inputs.requirements.optimisation_mode:
        case menus.OptimisationMode.RANDOM:
            return _random.add_random_objective_to_problem(
                problem=problem, variables=variables
            )
        case menus.OptimisationMode.NUTRIENT:
            return _nutrient.add_nutrient_objective_to_problem(
                problem=problem, inputs=inputs, variables=variables
            )
        case menus.OptimisationMode.VARIETY:
            return _variety.add_variety_objective_to_problem(
                problem=problem, inputs=inputs, variables=variables
            )
        case menus.OptimisationMode.SEMANTIC:
            return _semantic.add_semantic_objective_to_problem(
                problem=problem, inputs=inputs, variables=variables
            )
        case menus.OptimisationMode.EVERYTHING:
            return _add_everything_objective_to_problem(
                problem=problem, inputs=inputs, variables=variables
            )


def _add_everything_objective_to_problem(
    *,
    problem: lp.LpProblem,
    inputs: _inputs.OptimiserInputs,
    variables: _variables.Variables,
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

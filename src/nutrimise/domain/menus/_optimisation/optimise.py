from __future__ import annotations

import attrs
import pulp as lp

from nutrimise.domain import ingredients, menus, recipes

from . import constraints, inputs, objectives, variables


@attrs.frozen
class UnableToOptimiseMenu(Exception):
    menu_id: int


NoTargetsSet = objectives.NoTargetsSet

NoNutrientTargetsSet = objectives.NoNutrientTargetsSet

NoVarietyTargetsSet = objectives.NoVarietyTargetsSet


def optimise_recipes_for_menu(
    *,
    menu: menus.Menu,
    recipes_to_consider: tuple[recipes.Recipe, ...],
    relevant_ingredients: tuple[ingredients.Ingredient, ...],
) -> tuple[menus.MenuItem, ...]:
    """
    Express and solve the menu optimisation as an integer programming problem.

    :raises UnableToOptimiseMenu: If the solver did not find a solution.
    :raises NoTargetsSet: If the optimisation mode is `EVERYTHING` but
        no targets are set for any metric.
    :raises NoNutrientTargetsSet: If the optimisation mode is `NUTRIENT` but
        no nutrient targets have been set.
    :raises NoNutrientTargetsSet: If the optimisation mode is `INGREDIENT_VARIETY` but
        no ingredient variety targets have been set.
    """
    problem = lp.LpProblem(name=f"optimise-menu-{menu.id}")
    inputs_ = inputs.OptimiserInputs(
        menu=menu,
        recipes_to_consider=recipes_to_consider,
        relevant_ingredients=relevant_ingredients,
    )
    variables_ = variables.Variables.from_inputs(inputs_)
    for constraint in constraints.yield_all_constraints(
        inputs=inputs_, variables_=variables_
    ):
        problem += constraint
    problem = objectives.add_objective_to_problem(
        problem=problem, variables=variables_, inputs=inputs_
    )

    problem.solve(solver=lp.PULP_CBC_CMD(msg=False))
    if not problem.status == lp.constants.LpStatusOptimal:
        raise UnableToOptimiseMenu(menu_id=menu.id)

    solution = _extract_solution(decision_variables=variables_.decision_variables)
    return solution


def _extract_solution(
    *, decision_variables: tuple[variables.DecisionVariable, ...]
) -> tuple[menus.MenuItem, ...]:
    solution: list[menus.MenuItem] = []
    for variable in decision_variables:
        if variable.lp_variable.varValue == 1:
            variable.menu_item.update_recipe_id(recipe_id=variable.recipe.id)
            solution.append(variable.menu_item)
    return tuple(solution)

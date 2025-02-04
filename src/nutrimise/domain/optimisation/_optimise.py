from __future__ import annotations

import attrs
import pulp as lp

from nutrimise.domain import embeddings, ingredients, menus, recipes

from . import _constraints, _inputs, _objectives, _variables


NoTargetsSet = _objectives.NoTargetsSet

NoNutrientTargetsSet = _objectives.NoNutrientTargetsSet

NoVarietyTargetsSet = _objectives.NoVarietyTargetsSet


@attrs.frozen
class UnableToOptimiseMenu(Exception):
    menu_id: int

    def __str__(self) -> str:
        return "Menu requirements could not be met."


def optimise_recipes_for_menu(
    *,
    menu: menus.Menu,
    recipes_to_consider: tuple[recipes.Recipe, ...],
    relevant_ingredients: tuple[ingredients.Ingredient, ...],
    embedding_model: embeddings.EmbeddingModel | None = None,
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
    inputs_ = _inputs.OptimiserInputs(
        menu=menu,
        recipes_to_consider=recipes_to_consider,
        relevant_ingredients=relevant_ingredients,
        embedding_model=embedding_model,
    )
    variables = _variables.Variables.from_inputs(inputs_)
    for constraint in _constraints.yield_all_constraints(
        inputs=inputs_, variables_=variables
    ):
        problem += constraint
    problem = _objectives.add_objective_to_problem(
        problem=problem, variables=variables, inputs=inputs_
    )

    problem.solve(solver=lp.PULP_CBC_CMD(msg=False))
    if not problem.status == lp.constants.LpStatusOptimal:
        raise UnableToOptimiseMenu(menu_id=menu.id)

    solution = _extract_solution(decision_variables=variables.decision_variables)
    return solution


def _extract_solution(
    *, decision_variables: tuple[_variables.DecisionVariable, ...]
) -> tuple[menus.MenuItem, ...]:
    solution: list[menus.MenuItem] = []
    for variable in decision_variables:
        if variable.lp_variable.varValue == 1:
            variable.menu_item.update_recipe_id(recipe_id=variable.recipe.id)
            solution.append(variable.menu_item)
    return tuple(solution)

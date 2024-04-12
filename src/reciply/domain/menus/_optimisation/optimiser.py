from __future__ import annotations

import pulp as lp

from reciply.domain import menus, recipes

from . import constraints, variables


def optimise_recipes_for_menu(
    *,
    menu: menus.Menu,
    recipes_to_consider: tuple[recipes.Recipe, ...],
    # TODO -> will need to match by ID.
) -> tuple[menus.MenuItem, ...]:
    """
    Express and solve the menu optimisation as an integer programming problem.
    """
    problem = lp.LpProblem(name=f"optimise-menu-{menu.id}")
    variables_ = variables.Variables.from_spec(
        menu=menu, recipes_to_consider=recipes_to_consider
    )
    for constraint in constraints.yield_all_constraints(
        menu=menu, recipes_=recipes_to_consider, variables_=variables_
    ):
        problem += constraint
    problem.solve(solver=lp.PULP_CBC_CMD(msg=False))
    solution = _extract_solution(decision_variables=variables_.decision_variables)
    _verify_solution(solution=solution, menu=menu)
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


def _verify_solution(*, solution: tuple[menus.MenuItem, ...], menu: menus.Menu) -> None:
    pass

import pulp as lp

from reciply.data import constants

from . import variables


def sum_all_variables_for_menu_item(
    *, variables_: variables.Variables, menu_item_id: int
) -> lp.LpAffineExpression:
    """
    Get the sum of all the decision variables for a menu item.
    """
    return lp.lpSum(
        variable.lp_variable
        for variable in variables_.decision_variables
        if variable.menu_item.id == menu_item_id
    )


def sum_all_variables_for_recipe(
    *, variables_: variables.Variables, recipe_id: int
) -> lp.LpAffineExpression:
    """
    Get the sum of all the decision variables for a recipe.
    """
    return lp.lpSum(
        variable.lp_variable
        for variable in variables_.decision_variables
        if variable.recipe.id == recipe_id
    )


def total_nutrient_grams_for_day(
    *, variables_: variables.Variables, day: constants.Day, nutrient_id: int
) -> lp.LpAffineExpression:
    """
    Express the total grams of a nutrient in a menu on a day as a linear expression.

    As always, this is per serving.
    """
    total = lp.lpSum(0)
    for variable in variables_.decision_variables:
        if variable.day == day:
            nutrient_grams = _get_nutrient_grams_for_decision_variable(
                variable=variable, nutrient_id=nutrient_id
            )
            total += nutrient_grams
    return total


def _get_nutrient_grams_for_decision_variable(
    *, variable: variables.DecisionVariable, nutrient_id: int
) -> lp.LpAffineExpression:
    for nutritional_information in variable.recipe.nutritional_information_per_serving:
        if nutritional_information.nutrient.id == nutrient_id:
            return (
                nutritional_information.nutrient_quantity_grams * variable.lp_variable
            )
    return lp.lpSum(0)

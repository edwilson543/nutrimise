# Third party imports
import pulp as lp

# Local application imports
from reciply.data import constants

from . import variables


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
    for nutritional_information in variable.recipe.nutritional_information:
        if nutritional_information.nutrient.id == nutrient_id:
            return (
                nutritional_information.nutrient_quantity_grams * variable.lp_variable
            )
    return lp.lpSum(0)

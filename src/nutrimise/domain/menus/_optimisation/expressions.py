import pulp as lp

from nutrimise.data import constants

from . import inputs, variables


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


def number_of_occurrences_of_recipe(
    *, inputs: inputs.OptimiserInputs, variables_: variables.Variables, recipe_id: int
) -> lp.LpAffineExpression:
    """
    Get the sum of all the decision variables for a recipe.
    """
    existing_occurrences = 0
    for menu_item in inputs.menu.items:
        if menu_item.recipe_id == recipe_id and not menu_item.optimiser_generated:
            existing_occurrences += 1

    variables_sum = lp.lpSum(
        variable.lp_variable
        for variable in variables_.decision_variables
        if variable.recipe.id == recipe_id
    )
    return variables_sum + existing_occurrences


def total_nutrient_quantity_for_day(
    *,
    inputs: inputs.OptimiserInputs,
    variables: variables.Variables,
    day: constants.Day,
    nutrient_id: int,
) -> lp.LpAffineExpression:
    """
    Express the total quantity of a nutrient in a menu on a day as a linear expression.

    As always, this is per serving.
    """
    total = lp.lpSum(0)
    for variable in variables.decision_variables:
        if variable.day == day:
            nutrient_quantity = _get_nutrient_quantity_for_decision_variable(
                variable=variable, nutrient_id=nutrient_id
            )
            total += nutrient_quantity
    # Include the contribution from recipes selected for fixed times by the user.
    total += _get_unoptimised_nutrient_quantity_on_day(
        inputs=inputs, day=day, nutrient_id=nutrient_id
    )

    return total


def number_of_ingredients_in_category_across_menu(
    *,
    inputs: inputs.OptimiserInputs,
    variables: variables.Variables,
    ingedient_category_id: int,
) -> lp.LpAffineExpression:
    variable_contribution = lp.lpSum(
        [
            ingredient.lp_variable
            for ingredient in variables.ingredient_included_dependent_variables
            if ingredient.ingredient.category_id == ingedient_category_id
        ]
    )
    fixed_contribution = len(
        [
            ingredient
            for ingredient in inputs.unoptimised_ingredient_selections
            if ingredient.category_id == ingedient_category_id
        ]
    )
    return variable_contribution + fixed_contribution


def number_of_times_ingredient_features_across_menu(
    *, variables: variables.Variables, ingredient_id: int
) -> lp.LpAffineExpression:
    # Note: ingredients in unoptimised recipe selections are already accounted for.
    return lp.lpSum(
        decision_var.lp_variable
        for decision_var in variables.decision_variables
        if ingredient_id in decision_var.recipe.unique_ingredient_ids
    )


# Nutrition helpers.


def _get_nutrient_quantity_for_decision_variable(
    *, variable: variables.DecisionVariable, nutrient_id: int
) -> lp.LpAffineExpression:
    for nutritional_information in variable.recipe.nutritional_information_per_serving:
        if nutritional_information.nutrient.id == nutrient_id:
            return nutritional_information.nutrient_quantity * variable.lp_variable
    return lp.lpSum(0)


def _get_unoptimised_nutrient_quantity_on_day(
    *,
    inputs: inputs.OptimiserInputs,
    day: constants.Day,
    nutrient_id: int,
) -> float:
    total = 0.0
    for menu_item in inputs.menu.items:
        if menu_item.day == day and not menu_item.optimiser_generated:
            assert (recipe_id := menu_item.recipe_id) is not None  # Type narrowing.
            recipe = inputs.look_up_recipe(recipe_id=recipe_id)
            total += recipe.nutrient_quantity_per_serving(nutrient_id=nutrient_id)
    return total

from nutrimise.data import constants
from nutrimise.domain.menus._optimisation import inputs, variables

from tests.factories import domain as domain_factories


class TestFromSpec:
    def test_creates_decision_variable_for_each_recipe_occurring_at_each_menu_item(
        self,
    ):
        lunch = domain_factories.MenuItem(meal_time=constants.MealTime.LUNCH)
        dinner = domain_factories.MenuItem(meal_time=constants.MealTime.DINNER)
        menu = domain_factories.Menu(items=(lunch, dinner))

        recipe = domain_factories.Recipe(
            meal_times=[constants.MealTime.LUNCH, constants.MealTime.DINNER]
        )

        inputs_ = inputs.OptimiserInputs(
            menu=menu, recipes_to_consider=(recipe,), relevant_ingredients=()
        )
        variables_ = variables.Variables.from_inputs(inputs=inputs_)

        decision_variables = variables_.decision_variables
        assert len(decision_variables) == 2
        assert {variable.recipe.id for variable in decision_variables} == {recipe.id}
        assert {variable.menu_item.id for variable in decision_variables} == {
            lunch.id,
            dinner.id,
        }

    def test_does_not_create_decision_variable_for_recipe_not_matching_menu_item_meal_time(
        self,
    ):
        lunch = domain_factories.MenuItem(meal_time=constants.MealTime.LUNCH)
        dinner = domain_factories.MenuItem(meal_time=constants.MealTime.DINNER)
        menu = domain_factories.Menu(items=(lunch, dinner))

        recipe = domain_factories.Recipe(meal_times=[constants.MealTime.LUNCH])

        inputs_ = inputs.OptimiserInputs(
            menu=menu, recipes_to_consider=(recipe,), relevant_ingredients=()
        )
        variables_ = variables.Variables.from_inputs(inputs=inputs_)

        decision_variables = variables_.decision_variables
        assert len(decision_variables) == 1
        assert decision_variables[0].menu_item == lunch

    def test_does_not_create_decision_variable_for_menu_item_with_existing_recipe(self):
        lunch = domain_factories.MenuItem(
            meal_time=constants.MealTime.LUNCH, optimiser_generated=False
        )
        dinner = domain_factories.MenuItem(
            meal_time=constants.MealTime.DINNER, optimiser_generated=True
        )
        menu = domain_factories.Menu(items=(lunch, dinner))

        recipe = domain_factories.Recipe(
            meal_times=[constants.MealTime.LUNCH, constants.MealTime.DINNER]
        )

        inputs_ = inputs.OptimiserInputs(
            menu=menu, recipes_to_consider=(recipe,), relevant_ingredients=()
        )
        variables_ = variables.Variables.from_inputs(inputs=inputs_)

        decision_variables = variables_.decision_variables
        assert len(decision_variables) == 1
        assert decision_variables[0].menu_item == dinner

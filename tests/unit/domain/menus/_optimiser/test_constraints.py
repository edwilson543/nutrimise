from nutrimise.data import constants
from nutrimise.domain.menus._optimisation import constraints, inputs, variables

from tests.factories import domain as domain_factories


class TestNutrientGramsForDay:
    def test_sums_variables_for_given_day_only(self):
        nutrient = domain_factories.Nutrient()
        requirement = domain_factories.NutrientRequirement(
            minimum_quantity=11.25, maximum_quantity=4.75
        )

        # Creat a menu consisting of Monday lunch & dinner.
        monday_lunch = domain_factories.MenuItem(
            day=constants.Day.MONDAY, meal_time=constants.MealTime.LUNCH
        )
        monday_dinner = domain_factories.MenuItem(
            day=constants.Day.MONDAY, meal_time=constants.MealTime.DINNER
        )
        requirements = domain_factories.MenuRequirements(
            maximum_occurrences_per_recipe=1,
            nutrient_requirements=(requirement,),
        )
        menu = domain_factories.Menu(
            items=(monday_lunch, monday_dinner), requirements=requirements
        )

        # Create some recipes that could be had for both lunch and dinner
        nutritional_information = domain_factories.NutritionalInformation(
            nutrient=nutrient, nutrient_quantity=7.6
        )
        recipe = domain_factories.Recipe(
            nutritional_information_per_serving=(nutritional_information,),
            meal_times=[constants.MealTime.LUNCH, constants.MealTime.DINNER],
        )

        other_nutritional_information = domain_factories.NutritionalInformation(
            nutrient=nutrient, nutrient_quantity=9.1
        )
        other_recipe = domain_factories.Recipe(
            nutritional_information_per_serving=(other_nutritional_information,),
            meal_times=[constants.MealTime.LUNCH, constants.MealTime.DINNER],
        )

        inputs_ = inputs.OptimiserInputs(
            menu=menu,
            recipes_to_consider=(recipe, other_recipe),
            relevant_ingredients=(),
        )
        variables_ = variables.Variables.from_inputs(inputs_)

        all_constraints = [
            str(constraint)
            for constraint in constraints.yield_all_constraints(
                inputs=inputs_, variables_=variables_
            )
        ]

        expected_constraints = [
            # Menu items assignment constraints.
            f"recipe_{recipe.id}_for_menu_item_{monday_lunch.id} + recipe_{other_recipe.id}_for_menu_item_{monday_lunch.id} = 1",
            f"recipe_{recipe.id}_for_menu_item_{monday_dinner.id} + recipe_{other_recipe.id}_for_menu_item_{monday_dinner.id} = 1",
            # Maximum occurrences per recipe constraints.
            f"recipe_{recipe.id}_for_menu_item_{monday_lunch.id} + recipe_{recipe.id}_for_menu_item_{monday_dinner.id} <= 1",
            f"recipe_{other_recipe.id}_for_menu_item_{monday_lunch.id} + recipe_{other_recipe.id}_for_menu_item_{monday_dinner.id} <= 1",
            # Nutrient requirement constraints.
            f"7.6*recipe_{recipe.id}_for_menu_item_{monday_lunch.id} + 7.6*recipe_{recipe.id}_for_menu_item_{monday_dinner.id} + 9.1*recipe_{other_recipe.id}_for_menu_item_{monday_lunch.id} + 9.1*recipe_{other_recipe.id}_for_menu_item_{monday_dinner.id} >= {requirement.minimum_quantity}",
            f"7.6*recipe_{recipe.id}_for_menu_item_{monday_lunch.id} + 7.6*recipe_{recipe.id}_for_menu_item_{monday_dinner.id} + 9.1*recipe_{other_recipe.id}_for_menu_item_{monday_lunch.id} + 9.1*recipe_{other_recipe.id}_for_menu_item_{monday_dinner.id} <= {requirement.maximum_quantity}",
        ]

        assert all_constraints == expected_constraints

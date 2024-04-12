from reciply.data import constants
from reciply.domain.menus._optimisation import constraints, variables

from tests.factories import domain as domain_factories


class TestNutrientGramsForDay:
    def test_sums_variables_for_given_day_only(self):
        nutrient = domain_factories.Nutrient()
        requirement = domain_factories.NutrientRequirement(
            minimum_grams=11.25, maximum_grams=4.75
        )

        # Creat a menu consisting of Monday and Tuesday Lunch.
        monday_lunch = domain_factories.MenuItem(
            day=constants.Day.MONDAY, meal_time=constants.MealTime.LUNCH
        )
        monday_dinner = domain_factories.MenuItem(
            day=constants.Day.MONDAY, meal_time=constants.MealTime.DINNER
        )
        requirements = domain_factories.MenuRequirements(
            nutrient_requirements=(requirement,)
        )
        menu = domain_factories.Menu(
            items=(monday_lunch, monday_dinner), requirements=requirements
        )

        # Create a recipe that could be had for both lunch and dinner
        nutritional_information = domain_factories.NutritionalInformation(
            nutrient=nutrient, nutrient_quantity_grams=7.6
        )
        recipe = domain_factories.Recipe(
            nutritional_information_per_serving=(nutritional_information,),
            meal_times=[constants.MealTime.LUNCH, constants.MealTime.DINNER],
        )

        # Create the variables.
        variables_ = variables.Variables.from_spec(
            menu=menu, recipes_to_consider=(recipe,)
        )

        all_constraints = [
            str(constraint)
            for constraint in constraints.yield_all_constraints(
                menu=menu, variables_=variables_
            )
        ]

        expected_constraints = [
            f"7.6*recipe_{recipe.id}_for_menu_item_{monday_lunch.id} + 7.6*recipe_{recipe.id}_for_menu_item_{monday_dinner.id} >= {requirement.minimum_grams}",
            f"7.6*recipe_{recipe.id}_for_menu_item_{monday_lunch.id} + 7.6*recipe_{recipe.id}_for_menu_item_{monday_dinner.id} <= {requirement.maximum_grams}",
        ]

        assert all_constraints == expected_constraints

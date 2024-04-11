# Local application imports
from reciply.data import constants
from reciply.domain.menus._optimisation import expressions, variables
from tests.factories import domain as domain_factories


class TestNutrientGramsForDay:
    def test_sums_variables_for_given_day_only(self):
        # Creat a menu consisting of Monday and Tuesday Lunch.
        monday_lunch = domain_factories.MenuItem(
            day=constants.Day.MONDAY, meal_time=constants.MealTime.LUNCH
        )
        tuesday_lunch = domain_factories.MenuItem(
            day=constants.Day.TUESDAY, meal_time=constants.MealTime.LUNCH
        )
        menu = domain_factories.Menu(items=(monday_lunch, tuesday_lunch))

        nutrient = domain_factories.Nutrient()
        other_nutrient = domain_factories.Nutrient()

        # Create two recipes that could be used for Monday and or Tuesday lunch.
        nutritional_information = domain_factories.NutritionalInformation(
            nutrient=nutrient, nutrient_quantity_grams=2
        )
        other_nutritional_information = domain_factories.NutritionalInformation(
            nutrient=other_nutrient, nutrient_quantity_grams=7
        )
        recipe = domain_factories.Recipe(
            nutritional_information_per_serving=(
                nutritional_information,
                other_nutritional_information,
            ),
            meal_times=[constants.MealTime.LUNCH],
        )

        nutritional_information = domain_factories.NutritionalInformation(
            nutrient=nutrient, nutrient_quantity_grams=3
        )
        other_recipe = domain_factories.Recipe(
            nutritional_information_per_serving=(nutritional_information,),
            meal_times=[constants.MealTime.LUNCH],
        )

        # Create the variables.
        variables_ = variables.Variables.from_spec(
            menu=menu, recipes_to_consider=(recipe, other_recipe)
        )

        total_nutrient_grams = expressions.total_nutrient_grams_for_day(
            variables_=variables_, day=constants.Day.MONDAY, nutrient_id=nutrient.id
        )

        # Total nutrients should be summed over `MONDAY` and the `nutrient` only.
        assert (
            str(total_nutrient_grams)
            == f"2*recipe_{recipe.id}_for_menu_item_{monday_lunch.id} + 3*recipe_{other_recipe.id}_for_menu_item_{monday_lunch.id}"
        )

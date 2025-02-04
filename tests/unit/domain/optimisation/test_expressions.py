from nutrimise.domain import constants
from nutrimise.domain.optimisation import _expressions, _inputs, _variables
from testing.factories import domain as domain_factories


class TestNutrientGramsForDay:
    def test_sums_variables_for_given_day_only(self):
        # Creat a menu consisting of lunch for two days.
        day_one_lunch = domain_factories.MenuItem(
            day=1, meal_time=constants.MealTime.LUNCH
        )
        day_two_lunch = domain_factories.MenuItem(
            day=2, meal_time=constants.MealTime.LUNCH
        )
        menu = domain_factories.Menu(items=(day_one_lunch, day_two_lunch))

        nutrient = domain_factories.Nutrient()
        other_nutrient = domain_factories.Nutrient()

        # Create two recipes that could be used for Monday and or Tuesday lunch.
        nutritional_information = domain_factories.NutritionalInformation(
            nutrient=nutrient, nutrient_quantity=2
        )
        other_nutritional_information = domain_factories.NutritionalInformation(
            nutrient=other_nutrient, nutrient_quantity=7
        )
        recipe = domain_factories.Recipe(
            nutritional_information_per_serving=(
                nutritional_information,
                other_nutritional_information,
            ),
            meal_times=[constants.MealTime.LUNCH],
        )

        nutritional_information = domain_factories.NutritionalInformation(
            nutrient=nutrient, nutrient_quantity=3
        )
        other_recipe = domain_factories.Recipe(
            nutritional_information_per_serving=(nutritional_information,),
            meal_times=[constants.MealTime.LUNCH],
        )

        inputs_ = _inputs.OptimiserInputs(
            menu=menu,
            recipes_to_consider=(recipe, other_recipe),
            relevant_ingredients=(),
        )
        variables_ = _variables.Variables.from_inputs(inputs_)

        total_nutrient_quantity = _expressions.total_nutrient_quantity_for_day(
            inputs=inputs_,
            variables=variables_,
            day=day_one_lunch.day,
            nutrient_id=nutrient.id,
        )

        # Total nutrients should be summed over `MONDAY` and the `nutrient` only.
        options = [
            f"2*recipe_{recipe.id}_for_menu_item_{day_one_lunch.id} + 3*recipe_{other_recipe.id}_for_menu_item_{day_one_lunch.id}",
            f"3*recipe_{other_recipe.id}_for_menu_item_{day_one_lunch.id} + 2*recipe_{recipe.id}_for_menu_item_{day_one_lunch.id}",
        ]
        assert str(total_nutrient_quantity) in options

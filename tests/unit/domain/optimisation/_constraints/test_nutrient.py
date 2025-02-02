from nutrimise.domain import constants
from nutrimise.domain.optimisation import _inputs, _variables
from nutrimise.domain.optimisation._constraints import _nutrient
from tests.factories import domain as domain_factories


class TestNutrientConstraints:
    def test_constraints_minimum_and_maximum_nutrient_quantity(self):
        nutrient = domain_factories.Nutrient()
        requirement = domain_factories.NutrientRequirement(
            nutrient_id=nutrient.id, minimum_quantity=4.75, maximum_quantity=11.25
        )

        # Creat a menu consisting of lunch & dinner on the same day.
        lunch = domain_factories.MenuItem(meal_time=constants.MealTime.LUNCH)
        dinner = domain_factories.MenuItem(
            day=lunch.day, meal_time=constants.MealTime.DINNER
        )
        requirements = domain_factories.MenuRequirements(
            maximum_occurrences_per_recipe=1,
            nutrient_requirements=(requirement,),
        )
        menu = domain_factories.Menu(items=(lunch, dinner), requirements=requirements)

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

        inputs_ = _inputs.OptimiserInputs(
            menu=menu,
            recipes_to_consider=(recipe, other_recipe),
            relevant_ingredients=(),
        )
        variables_ = _variables.Variables.from_inputs(inputs_)

        all_constraints = {
            str(constraint)
            for constraint in _nutrient.all_nutrient_requirements_are_met(
                inputs=inputs_, variables_=variables_
            )
        }

        nutrient_requirement_constraints = {
            f"7.6*recipe_{recipe.id}_for_menu_item_{lunch.id} + 7.6*recipe_{recipe.id}_for_menu_item_{dinner.id} + 9.1*recipe_{other_recipe.id}_for_menu_item_{lunch.id} + 9.1*recipe_{other_recipe.id}_for_menu_item_{dinner.id} >= {requirement.minimum_quantity}",
            f"7.6*recipe_{recipe.id}_for_menu_item_{lunch.id} + 7.6*recipe_{recipe.id}_for_menu_item_{dinner.id} + 9.1*recipe_{other_recipe.id}_for_menu_item_{lunch.id} + 9.1*recipe_{other_recipe.id}_for_menu_item_{dinner.id} <= {requirement.maximum_quantity}",
        }

        assert nutrient_requirement_constraints == all_constraints

from nutrimise.domain.menus._optimisation import inputs, variables
from nutrimise.domain.menus._optimisation.constraints import _fulfillment
from tests.factories import domain as domain_factories


class TestFulfillmentConstraints:
    def test_constraints_that_all_menu_items_are_assigned_a_recipe(self):
        # Creat a menu with one empty item.
        menu_item = domain_factories.MenuItem()
        requirements = domain_factories.MenuRequirements(
            maximum_occurrences_per_recipe=1
        )
        menu = domain_factories.Menu(items=(menu_item,), requirements=requirements)

        # Create two recipes that could fulfill the menu item
        recipe = domain_factories.Recipe(meal_times=[menu_item.meal_time])
        other_recipe = domain_factories.Recipe(meal_times=[menu_item.meal_time])

        inputs_ = inputs.OptimiserInputs(
            menu=menu,
            recipes_to_consider=(recipe, other_recipe),
            relevant_ingredients=(),
        )
        variables_ = variables.Variables.from_inputs(inputs_)

        all_constraints = [
            str(constraint)
            for constraint in _fulfillment.all_menu_items_are_assigned_a_recipe(
                inputs=inputs_, variables_=variables_
            )
        ]

        expected_constraints = [
            f"recipe_{recipe.id}_for_menu_item_{menu_item.id} + recipe_{other_recipe.id}_for_menu_item_{menu_item.id} = 1",
        ]

        assert all_constraints == expected_constraints

    def test_constraints_maximum_uses_of_a_recipe(self):
        # Creat a menu with one empty item.
        menu_item = domain_factories.MenuItem()
        requirements = domain_factories.MenuRequirements(
            maximum_occurrences_per_recipe=1
        )
        menu = domain_factories.Menu(items=(menu_item,), requirements=requirements)

        # Create two recipes that could fulfill the menu item
        recipe = domain_factories.Recipe(meal_times=[menu_item.meal_time])
        other_recipe = domain_factories.Recipe(meal_times=[menu_item.meal_time])

        inputs_ = inputs.OptimiserInputs(
            menu=menu,
            recipes_to_consider=(recipe, other_recipe),
            relevant_ingredients=(),
        )
        variables_ = variables.Variables.from_inputs(inputs_)

        all_constraints = [
            str(constraint)
            for constraint in _fulfillment.recipes_do_not_exceed_maximum_occurrences(
                inputs=inputs_, variables_=variables_
            )
        ]

        expected_constraints = [
            f"recipe_{recipe.id}_for_menu_item_{menu_item.id} <= 1",
            f"recipe_{other_recipe.id}_for_menu_item_{menu_item.id} <= 1",
        ]

        assert all_constraints == expected_constraints

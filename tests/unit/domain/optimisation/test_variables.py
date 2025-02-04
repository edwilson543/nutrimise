from nutrimise.domain import constants
from nutrimise.domain.optimisation import _inputs, _variables
from testing.factories import domain as domain_factories


class TestFromSpecDecisionVariables:
    def test_creates_decision_variable_for_each_recipe_occurring_at_each_menu_item(
        self,
    ):
        lunch = domain_factories.MenuItem(meal_time=constants.MealTime.LUNCH)
        dinner = domain_factories.MenuItem(meal_time=constants.MealTime.DINNER)
        menu = domain_factories.Menu(items=(lunch, dinner))

        recipe = domain_factories.Recipe(
            meal_times=[constants.MealTime.LUNCH, constants.MealTime.DINNER]
        )

        inputs_ = _inputs.OptimiserInputs(
            menu=menu, recipes_to_consider=(recipe,), relevant_ingredients=()
        )
        variables_ = _variables.Variables.from_inputs(inputs=inputs_)

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

        inputs_ = _inputs.OptimiserInputs(
            menu=menu, recipes_to_consider=(recipe,), relevant_ingredients=()
        )
        variables_ = _variables.Variables.from_inputs(inputs=inputs_)

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

        inputs_ = _inputs.OptimiserInputs(
            menu=menu, recipes_to_consider=(recipe,), relevant_ingredients=()
        )
        variables_ = _variables.Variables.from_inputs(inputs=inputs_)

        decision_variables = variables_.decision_variables
        assert len(decision_variables) == 1
        assert decision_variables[0].menu_item == dinner


class TestFromInclusionDependentVariables:
    def test_creates_inclusion_dependent_variable_for_recipe_and_ingredient(self):
        ingredient = domain_factories.Ingredient()
        recipe_ingredient = domain_factories.RecipeIngredient(
            ingredient_id=ingredient.id
        )
        recipe = domain_factories.Recipe(ingredients=(recipe_ingredient,))

        inputs_ = _inputs.OptimiserInputs(
            menu=domain_factories.Menu(),
            recipes_to_consider=(recipe,),
            relevant_ingredients=(ingredient,),
        )
        variables_ = _variables.Variables.from_inputs(inputs=inputs_)

        ingredient_included_variables = (
            variables_.ingredient_included_dependent_variables
        )
        assert len(ingredient_included_variables) == 1
        ingredient_included_variable = ingredient_included_variables[0]
        assert ingredient_included_variable.ingredient == ingredient
        assert ingredient_included_variable.lp_variable is not None

    def test_does_not_create_inclusion_dependent_variable_for_unoptimised_ingredients(
        self,
    ):
        ingredient = domain_factories.Ingredient()
        recipe = domain_factories.Recipe(
            ingredients=(
                domain_factories.RecipeIngredient(ingredient_id=ingredient.id),
            )
        )

        other_ingredient = domain_factories.Ingredient()
        other_recipe = domain_factories.Recipe(
            ingredients=(
                domain_factories.RecipeIngredient(ingredient_id=ingredient.id),
                domain_factories.RecipeIngredient(ingredient_id=other_ingredient.id),
            )
        )

        # Force `recipe` to be included in the menu.
        unoptimised_selection = domain_factories.MenuItem(
            recipe_id=recipe.id, optimiser_generated=False
        )
        menu = domain_factories.Menu(items=(unoptimised_selection,))

        inputs_ = _inputs.OptimiserInputs(
            menu=menu,
            recipes_to_consider=(recipe, other_recipe),
            relevant_ingredients=(ingredient, other_ingredient),
        )
        variables_ = _variables.Variables.from_inputs(inputs=inputs_)

        # There should be no inclusion variable for `ingredient`, since it features in `recipe`.
        ingredient_included_variables = (
            variables_.ingredient_included_dependent_variables
        )
        assert len(ingredient_included_variables) == 1
        ingredient_included_variable = ingredient_included_variables[0]
        assert ingredient_included_variable.ingredient == other_ingredient

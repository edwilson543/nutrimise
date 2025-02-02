from unittest import mock

import pytest

from nutrimise.domain import constants, menus, optimisation, recipes
from tests.factories import domain as domain_factories


def _lunch_and_dinner_menu(
    *,
    requirements: menus.MenuRequirements | None = None,
    lunch: recipes.Recipe | None = None,
    dinner: recipes.Recipe | None = None,
):
    lunch = domain_factories.MenuItem(
        meal_time=constants.MealTime.LUNCH,
        recipe_id=lunch.id if lunch else None,
        optimiser_generated=lunch is None,
    )
    dinner = dinner or domain_factories.MenuItem(
        day=lunch.day,
        meal_time=constants.MealTime.DINNER,
        recipe_id=dinner.id if dinner else None,
        optimiser_generated=dinner is None,
    )
    requirements = requirements or domain_factories.MenuRequirements()
    return domain_factories.Menu(items=(lunch, dinner), requirements=requirements)


class TestBasicRequirements:
    def test_respects_menu_item_assignment_constraints(self):
        menu_item = domain_factories.MenuItem(recipe_id=None)
        menu = domain_factories.Menu(items=[menu_item])
        recipe = domain_factories.Recipe(meal_times=[menu_item.meal_time])

        solution = optimisation.optimise_recipes_for_menu(
            menu=menu, recipes_to_consider=(recipe,), relevant_ingredients=()
        )

        assert len(solution) == 1
        assert solution[0].recipe_id == recipe.id

    def test_respects_recipe_meal_time_restrictions(self):
        menu = _lunch_and_dinner_menu()

        lunch_recipe = domain_factories.Recipe(meal_times=[constants.MealTime.LUNCH])
        dinner_recipe = domain_factories.Recipe(meal_times=[constants.MealTime.DINNER])

        solution = optimisation.optimise_recipes_for_menu(
            menu=menu,
            recipes_to_consider=(lunch_recipe, dinner_recipe),
            relevant_ingredients=(),
        )

        assert len(solution) == 2
        assert solution[0].recipe_id == lunch_recipe.id
        assert solution[1].recipe_id == dinner_recipe.id

    def test_raises_if_insufficient_recipes_are_considered(self):
        menu_item = domain_factories.MenuItem(recipe_id=None)
        menu = domain_factories.Menu(items=[menu_item])

        with pytest.raises(optimisation.UnableToOptimiseMenu) as exc:
            optimisation.optimise_recipes_for_menu(
                menu=menu, recipes_to_consider=(), relevant_ingredients=()
            )

        assert exc.value.menu_id == menu.id


class TestMaximumRecipeOccurrencesPerRecipeConstraints:
    def test_respects_maximum_occurrences_per_recipe_constraint(self):
        requirements = domain_factories.MenuRequirements(
            maximum_occurrences_per_recipe=1
        )
        menu = _lunch_and_dinner_menu(requirements=requirements)

        meal_times = [constants.MealTime.LUNCH, constants.MealTime.DINNER]
        recipe = domain_factories.Recipe(meal_times=meal_times)
        other_recipe = domain_factories.Recipe(meal_times=meal_times)

        solution = optimisation.optimise_recipes_for_menu(
            menu=menu,
            recipes_to_consider=(recipe, other_recipe),
            relevant_ingredients=(),
        )

        assert len(solution) == 2
        assert {item.recipe_id for item in solution} == {recipe.id, other_recipe.id}

    def test_unoptimised_selection_contributes_to_maximum_occurrences_per_recipe_constraint(
        self,
    ):
        meal_times = [constants.MealTime.LUNCH, constants.MealTime.DINNER]
        pre_selected_recipe = domain_factories.Recipe(meal_times=meal_times)
        other_recipe = domain_factories.Recipe(meal_times=meal_times)

        requirements = domain_factories.MenuRequirements(
            maximum_occurrences_per_recipe=1
        )
        menu = _lunch_and_dinner_menu(
            requirements=requirements, lunch=pre_selected_recipe, dinner=None
        )

        solution = optimisation.optimise_recipes_for_menu(
            menu=menu,
            recipes_to_consider=(pre_selected_recipe, other_recipe),
            relevant_ingredients=(),
        )

        assert len(solution) == 1
        assert solution[0].recipe_id == other_recipe.id


class TestNutrientRequirements:
    def test_respects_minimum_nutrient_requirement_constraint(self):
        nutrient = domain_factories.Nutrient()
        minimum_quantity = 10

        high_nutrition_recipe = domain_factories.Recipe.any_meal_time_with_nutrient(
            nutrient=nutrient, nutrient_quantity=minimum_quantity + 1
        )
        low_nutrition_recipe = domain_factories.Recipe.any_meal_time_with_nutrient(
            nutrient=nutrient, nutrient_quantity=minimum_quantity - 1
        )

        menu_item = domain_factories.MenuItem(
            recipe_id=None, meal_time=constants.MealTime.LUNCH
        )
        nutrition_requirement = domain_factories.NutrientRequirement(
            nutrient_id=nutrient.id, minimum_quantity=minimum_quantity
        )
        menu_requirements = domain_factories.MenuRequirements(
            nutrient_requirements=(nutrition_requirement,)
        )
        menu = domain_factories.Menu(items=[menu_item], requirements=menu_requirements)

        solution = optimisation.optimise_recipes_for_menu(
            menu=menu,
            recipes_to_consider=(low_nutrition_recipe, high_nutrition_recipe),
            relevant_ingredients=(),
        )

        assert len(solution) == 1
        assert solution[0].recipe_id == high_nutrition_recipe.id

    def test_respects_minimum_nutrient_requirement_constraint_with_fixed_item(self):
        nutrient = domain_factories.Nutrient()
        nutrition_requirement = domain_factories.NutrientRequirement(
            nutrient_id=nutrient.id, minimum_quantity=10
        )
        lunch_nutrient_quantity = nutrition_requirement.minimum_quantity / 2
        min_dinner_nutrient_quantity = (
            nutrition_requirement.minimum_quantity - lunch_nutrient_quantity
        )

        # Create two dinner options that can make up the nutrition deficit.
        lunch_recipe = domain_factories.Recipe.any_meal_time_with_nutrient(
            nutrient=nutrient, nutrient_quantity=lunch_nutrient_quantity
        )
        ideal_dinner = domain_factories.Recipe.any_meal_time_with_nutrient(
            nutrient=nutrient, nutrient_quantity=min_dinner_nutrient_quantity + 1
        )
        suboptimal_dinner = domain_factories.Recipe.any_meal_time_with_nutrient(
            nutrient=nutrient, nutrient_quantity=min_dinner_nutrient_quantity - 1
        )

        # Create a menu with lunch already selected.
        menu_requirements = domain_factories.MenuRequirements(
            nutrient_requirements=(nutrition_requirement,),
            maximum_occurrences_per_recipe=1,  # To avoid the lunch recipe getting selected for dinner.
        )
        menu = _lunch_and_dinner_menu(
            requirements=menu_requirements, lunch=lunch_recipe, dinner=None
        )

        solution = optimisation.optimise_recipes_for_menu(
            menu=menu,
            recipes_to_consider=(lunch_recipe, ideal_dinner, suboptimal_dinner),
            relevant_ingredients=(),
        )

        assert len(solution) == 1
        assert solution[0].recipe_id == ideal_dinner.id

    def test_respects_maximum_nutrient_requirement_constraint(self):
        nutrient = domain_factories.Nutrient()
        maximum_quantity = 10

        # Create two recipes above / below the minimum nutrient requirements.
        low_nutrition_recipe = domain_factories.Recipe.any_meal_time_with_nutrient(
            nutrient=nutrient, nutrient_quantity=maximum_quantity - 1
        )
        high_nutrition_recipe = domain_factories.Recipe.any_meal_time_with_nutrient(
            nutrient=nutrient, nutrient_quantity=maximum_quantity + 1
        )

        menu_item = domain_factories.MenuItem(
            recipe_id=None, meal_time=constants.MealTime.LUNCH
        )
        nutrition_requirement = domain_factories.NutrientRequirement(
            nutrient_id=nutrient.id, maximum_quantity=maximum_quantity
        )
        menu_requirements = domain_factories.MenuRequirements(
            nutrient_requirements=(nutrition_requirement,)
        )
        menu = domain_factories.Menu(items=[menu_item], requirements=menu_requirements)

        solution = optimisation.optimise_recipes_for_menu(
            menu=menu,
            recipes_to_consider=(low_nutrition_recipe, high_nutrition_recipe),
            relevant_ingredients=(),
        )

        assert len(solution) == 1
        assert solution[0].recipe_id == low_nutrition_recipe.id

    def test_respects_maximum_nutrient_requirement_constraint_with_fixed_item(self):
        nutrient = domain_factories.Nutrient()
        nutrition_requirement = domain_factories.NutrientRequirement(
            nutrient_id=nutrient.id, maximum_quantity=8.3
        )
        lunch_nutrient_quantity = nutrition_requirement.maximum_quantity / 2
        max_dinner_nutrient = (
            nutrition_requirement.maximum_quantity - lunch_nutrient_quantity
        )

        # Create two dinner options.
        lunch_recipe = domain_factories.Recipe.any_meal_time_with_nutrient(
            nutrient=nutrient, nutrient_quantity=lunch_nutrient_quantity
        )
        ideal_dinner = domain_factories.Recipe.any_meal_time_with_nutrient(
            nutrient=nutrient, nutrient_quantity=max_dinner_nutrient - 1
        )
        suboptimal_dinner = domain_factories.Recipe.any_meal_time_with_nutrient(
            nutrient=nutrient, nutrient_quantity=max_dinner_nutrient + 1
        )

        # Create a menu with lunch already selected.
        menu_requirements = domain_factories.MenuRequirements(
            nutrient_requirements=(nutrition_requirement,),
            maximum_occurrences_per_recipe=1,  # To avoid the lunch recipe getting selected for dinner.
        )
        menu = _lunch_and_dinner_menu(
            requirements=menu_requirements, lunch=lunch_recipe, dinner=None
        )

        solution = optimisation.optimise_recipes_for_menu(
            menu=menu,
            recipes_to_consider=(lunch_recipe, ideal_dinner, suboptimal_dinner),
            relevant_ingredients=(),
        )

        assert len(solution) == 1
        assert solution[0].recipe_id == ideal_dinner.id


class TestVarietyRequirements:
    def test_respects_minimum_variety_requirement_constraint(self):
        # Create two ingredients in the same category.
        category_id = 1
        ingredient = domain_factories.Ingredient(category_id=category_id)
        other_ingredient = domain_factories.Ingredient(category_id=category_id)

        # Create a menu needing a single recipe, with two ingredients in the given category.
        variety_requirement = domain_factories.VarietyRequirement(
            ingredient_category_id=ingredient.category_id, minimum=2
        )
        menu_requirements = domain_factories.MenuRequirements(
            variety_requirements=(variety_requirement,)
        )
        menu_item = domain_factories.MenuItem(recipe_id=None)
        menu = domain_factories.Menu(items=[menu_item], requirements=menu_requirements)

        # Create a recipe with / without sufficient ingredients in the required category.
        ideal_recipe = domain_factories.Recipe.with_ingredients(
            ingredients=[ingredient, other_ingredient], meal_times=[menu_item.meal_time]
        )
        suboptimal_recipe = domain_factories.Recipe.with_ingredients(
            ingredients=[ingredient], meal_times=[menu_item.meal_time]
        )

        solution = optimisation.optimise_recipes_for_menu(
            menu=menu,
            recipes_to_consider=(
                ideal_recipe,
                suboptimal_recipe,
            ),
            relevant_ingredients=(ingredient, other_ingredient),
        )

        assert len(solution) == 1
        assert solution[0].recipe_id == ideal_recipe.id

    def test_respects_maximum_variety_requirement_constraint(self):
        # Create a menu needing a single recipe selecting.
        ingredient = domain_factories.Ingredient()
        variety_requirement = domain_factories.VarietyRequirement(
            ingredient_category_id=ingredient.category_id, maximum=0
        )
        menu_requirements = domain_factories.MenuRequirements(
            variety_requirements=(variety_requirement,)
        )
        menu_item = domain_factories.MenuItem(recipe_id=None)
        menu = domain_factories.Menu(items=[menu_item], requirements=menu_requirements)

        # Create a recipe with / without an ingredient in the required category.
        recipe_with_ingredient_in_category = domain_factories.Recipe.with_ingredients(
            ingredients=[ingredient], meal_times=[menu_item.meal_time]
        )
        recipe_without_ingredient_in_category = (
            domain_factories.Recipe.with_ingredients(
                ingredients=[], meal_times=[menu_item.meal_time]
            )
        )

        solution = optimisation.optimise_recipes_for_menu(
            menu=menu,
            recipes_to_consider=(
                recipe_with_ingredient_in_category,
                recipe_without_ingredient_in_category,
            ),
            relevant_ingredients=(ingredient,),
        )

        assert len(solution) == 1
        assert solution[0].recipe_id == recipe_without_ingredient_in_category.id

    def test_respects_minimum_and_maximum_variety_requirement(self):
        # Create a menu needing a single recipe selecting.
        ingredient_category_id = 123
        requirement = 2
        variety_requirement = domain_factories.VarietyRequirement(
            ingredient_category_id=ingredient_category_id,
            minimum=requirement,
            maximum=requirement,
        )
        menu_requirements = domain_factories.MenuRequirements(
            variety_requirements=(variety_requirement,)
        )
        menu_item = domain_factories.MenuItem(recipe_id=None)
        menu = domain_factories.Menu(items=[menu_item], requirements=menu_requirements)

        # Create recipes with 0-3 ingredients in the required category.
        n_recipes_to_create = requirement + 1
        relevant_ingredients = tuple(
            domain_factories.Ingredient(category_id=ingredient_category_id)
            for _ in range(0, n_recipes_to_create + 1)
        )

        recipes_to_consider = tuple(
            domain_factories.Recipe.with_ingredients(
                ingredients=relevant_ingredients[:n_ingredients],
                meal_times=[menu_item.meal_time],
            )
            for n_ingredients in range(0, n_recipes_to_create + 1)
        )
        only_recipe_meeting_requirement = recipes_to_consider[requirement]

        solution = optimisation.optimise_recipes_for_menu(
            menu=menu,
            recipes_to_consider=recipes_to_consider,
            relevant_ingredients=relevant_ingredients,
        )

        assert len(solution) == 1
        assert solution[0].recipe_id == only_recipe_meeting_requirement.id

    def test_unoptimised_recipe_selection_counts_towards_variety_requirement(self):
        category_id = 1
        ingredient = domain_factories.Ingredient(category_id=category_id)
        other_ingredient = domain_factories.Ingredient(category_id=category_id)

        lunch_recipe = domain_factories.Recipe.with_ingredients(
            ingredients=[ingredient], meal_times=[constants.MealTime.LUNCH]
        )
        ideal_dinner_recipe = domain_factories.Recipe.with_ingredients(
            ingredients=[other_ingredient], meal_times=[constants.MealTime.DINNER]
        )
        suboptimal_dinner_recipe = domain_factories.Recipe(
            ingredients=[], meal_times=[constants.MealTime.DINNER]
        )

        # Create a menu with lunch already selected, but requiring dinner selecting.
        variety_requirement = domain_factories.VarietyRequirement(
            ingredient_category_id=category_id,
            minimum=2,
        )
        menu_requirements = domain_factories.MenuRequirements(
            variety_requirements=(variety_requirement,)
        )
        menu = _lunch_and_dinner_menu(
            requirements=menu_requirements, lunch=lunch_recipe
        )

        solution = optimisation.optimise_recipes_for_menu(
            menu=menu,
            recipes_to_consider=(
                lunch_recipe,
                ideal_dinner_recipe,
                suboptimal_dinner_recipe,
            ),
            relevant_ingredients=(ingredient, other_ingredient),
        )

        assert len(solution) == 1
        assert solution[0].recipe_id == ideal_dinner_recipe.id


class TestRandomObjective:
    @mock.patch("random.random", side_effect=[0.5, 0.1])
    def test_random_objective_decides_selected_recipe(self, mock_random: mock.Mock):
        requirements = domain_factories.MenuRequirements(
            optimisation_mode=constants.OptimisationMode.RANDOM
        )
        item = domain_factories.MenuItem()
        menu = domain_factories.Menu(items=(item,), requirements=requirements)

        # `random.random` is mocked to favour the latter recipe (the second mock
        # value is lower, order is preserved, and the optimisation sense is minimise).
        recipe = domain_factories.Recipe(meal_times=[item.meal_time])
        favoured_recipe = domain_factories.Recipe(meal_times=[item.meal_time])

        solution = optimisation.optimise_recipes_for_menu(
            menu=menu,
            recipes_to_consider=(recipe, favoured_recipe),
            relevant_ingredients=(),
        )

        assert len(solution) == 1
        assert solution[0].recipe_id == favoured_recipe.id


class TestNutrientObjective:
    # Include a recipe above / below the target to ensure we aren't just minimizing / maximizing.
    @pytest.mark.parametrize("suboptimal_deviation", [-5, 5])
    @pytest.mark.parametrize(
        "optimisation_mode",
        [constants.OptimisationMode.NUTRIENT, constants.OptimisationMode.EVERYTHING],
    )
    def test_nutrient_objective_forces_recipe_selection_with_target_nutrient_content(
        self, suboptimal_deviation: int, optimisation_mode: constants.OptimisationMode
    ):
        nutrient = domain_factories.Nutrient()
        target_quantity = 10
        nutrient_requirement = domain_factories.NutrientRequirement(
            nutrient_id=nutrient.id, target_quantity=target_quantity
        )
        requirements = domain_factories.MenuRequirements(
            optimisation_mode=optimisation_mode,
            nutrient_requirements=(nutrient_requirement,),
        )
        item = domain_factories.MenuItem()
        menu = domain_factories.Menu(items=(item,), requirements=requirements)

        optimal_recipe = domain_factories.Recipe.any_meal_time_with_nutrient(
            nutrient=nutrient, nutrient_quantity=target_quantity
        )
        suboptimal_recipe = domain_factories.Recipe.any_meal_time_with_nutrient(
            nutrient=nutrient, nutrient_quantity=target_quantity + suboptimal_deviation
        )

        solution = optimisation.optimise_recipes_for_menu(
            menu=menu,
            recipes_to_consider=(optimal_recipe, suboptimal_recipe),
            relevant_ingredients=(),
        )

        assert len(solution) == 1
        assert solution[0].recipe_id == optimal_recipe.id

    def test_raises_when_no_nutrient_targets_set(self):
        requirements = domain_factories.MenuRequirements(
            optimisation_mode=constants.OptimisationMode.NUTRIENT,
        )
        item = domain_factories.MenuItem()
        menu = domain_factories.Menu(items=(item,), requirements=requirements)

        recipe = domain_factories.Recipe()

        with pytest.raises(optimisation.NoNutrientTargetsSet) as exc:
            optimisation.optimise_recipes_for_menu(
                menu=menu,
                recipes_to_consider=(recipe,),
                relevant_ingredients=(),
            )

        assert exc.value.menu_id == menu.id


class TestVarietyObjective:
    @pytest.mark.parametrize("target", [0, 1])
    @pytest.mark.parametrize(
        "optimisation_mode",
        [constants.OptimisationMode.VARIETY, constants.OptimisationMode.EVERYTHING],
    )
    def test_variety_objective_forces_selection_of_recipe_containing_ingredient(
        self, optimisation_mode: constants.OptimisationMode, target: int
    ):
        ingredient = domain_factories.Ingredient()
        variety_requirement = domain_factories.VarietyRequirement(
            ingredient_category_id=ingredient.category_id,
            target=target,
        )
        requirements = domain_factories.MenuRequirements(
            optimisation_mode=optimisation_mode,
            variety_requirements=(variety_requirement,),
        )
        item = domain_factories.MenuItem()
        menu = domain_factories.Menu(items=(item,), requirements=requirements)

        with_ingredient_recipe = domain_factories.Recipe.with_ingredients(
            ingredients=[ingredient], meal_times=[item.meal_time]
        )
        without_ingredient_recipe = domain_factories.Recipe.with_ingredients(
            ingredients=[], meal_times=[item.meal_time]
        )

        solution = optimisation.optimise_recipes_for_menu(
            menu=menu,
            recipes_to_consider=(with_ingredient_recipe, without_ingredient_recipe),
            relevant_ingredients=(ingredient,),
        )

        assert len(solution) == 1
        optimal_recipe = {0: without_ingredient_recipe, 1: with_ingredient_recipe}[
            target
        ]
        assert solution[0].recipe_id == optimal_recipe.id

    def test_raises_when_no_variety_targets_set(self):
        requirements = domain_factories.MenuRequirements(
            optimisation_mode=constants.OptimisationMode.VARIETY,
        )
        item = domain_factories.MenuItem()
        menu = domain_factories.Menu(items=(item,), requirements=requirements)

        recipe = domain_factories.Recipe()

        with pytest.raises(optimisation.NoVarietyTargetsSet) as exc:
            optimisation.optimise_recipes_for_menu(
                menu=menu,
                recipes_to_consider=(recipe,),
                relevant_ingredients=(),
            )

        assert exc.value.menu_id == menu.id


class TestEverythingObjective:
    def test_raises_when_no_targets_are_set(self):
        requirements = domain_factories.MenuRequirements(
            optimisation_mode=constants.OptimisationMode.EVERYTHING,
        )
        item = domain_factories.MenuItem()
        menu = domain_factories.Menu(items=(item,), requirements=requirements)

        recipe = domain_factories.Recipe()

        with pytest.raises(optimisation.NoTargetsSet) as exc:
            optimisation.optimise_recipes_for_menu(
                menu=menu,
                recipes_to_consider=(recipe,),
                relevant_ingredients=(),
            )

        assert exc.value.menu_id == menu.id

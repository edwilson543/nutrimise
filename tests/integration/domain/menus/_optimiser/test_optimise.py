from reciply.data import constants
from reciply.domain import menus, recipes

from tests.factories import domain as domain_factories
import pytest


def _lunch_and_dinner_menu(
    *,
    requirements: menus.MenuRequirements | None = None,
    lunch: recipes.Recipe | None = None,
    dinner: recipes.Recipe | None = None,
):
    lunch = domain_factories.MenuItem(
        day=constants.Day.MONDAY,
        meal_time=constants.MealTime.LUNCH,
        recipe_id=lunch.id if lunch else None,
        optimiser_generated=lunch is None,
    )
    dinner = dinner or domain_factories.MenuItem(
        day=constants.Day.MONDAY,
        meal_time=constants.MealTime.DINNER,
        recipe_id=dinner.id if dinner else None,
        optimiser_generated=dinner is None,
    )
    requirements = requirements or domain_factories.MenuRequirements()
    return domain_factories.Menu(items=(lunch, dinner), requirements=requirements)


# Basic requirements.


def test_respects_menu_item_assignment_constraints():
    menu_item = domain_factories.MenuItem(recipe_id=None)
    menu = domain_factories.Menu(items=[menu_item])
    recipe = domain_factories.Recipe(meal_times=[menu_item.meal_time])

    solution = menus.optimise_recipes_for_menu(menu=menu, recipes_to_consider=(recipe,))

    assert len(solution) == 1
    assert solution[0].recipe_id == recipe.id


def test_respects_recipe_meal_time_restrictions():
    menu = _lunch_and_dinner_menu()

    lunch_recipe = domain_factories.Recipe(meal_times=[constants.MealTime.LUNCH])
    dinner_recipe = domain_factories.Recipe(meal_times=[constants.MealTime.DINNER])

    solution = menus.optimise_recipes_for_menu(
        menu=menu, recipes_to_consider=(lunch_recipe, dinner_recipe)
    )

    assert len(solution) == 2
    assert solution[0].recipe_id == lunch_recipe.id
    assert solution[1].recipe_id == dinner_recipe.id


def test_raises_if_insufficient_recipes_are_considered():
    menu_item = domain_factories.MenuItem(recipe_id=None)
    menu = domain_factories.Menu(items=[menu_item])

    with pytest.raises(menus.UnableToOptimiseMenu) as exc:
        menus.optimise_recipes_for_menu(menu=menu, recipes_to_consider=())

    assert exc.value.menu_id == menu.id


# Maximum recipe occurrences requirements.


def test_respects_maximum_occurrences_per_recipe_constraint():
    menu = _lunch_and_dinner_menu()

    meal_times = [constants.MealTime.LUNCH, constants.MealTime.DINNER]
    recipe = domain_factories.Recipe(meal_times=meal_times)
    other_recipe = domain_factories.Recipe(meal_times=meal_times)

    solution = menus.optimise_recipes_for_menu(
        menu=menu, recipes_to_consider=(recipe, other_recipe)
    )

    assert len(solution) == 2
    assert {item.recipe_id for item in solution} == {recipe.id, other_recipe.id}


def test_unoptimised_selection_contributes_to_maximum_occurrences_per_recipe_constraint():
    meal_times = [constants.MealTime.LUNCH, constants.MealTime.DINNER]
    pre_selected_recipe = domain_factories.Recipe(meal_times=meal_times)
    other_recipe = domain_factories.Recipe(meal_times=meal_times)

    requirements = domain_factories.MenuRequirements(maximum_occurrences_per_recipe=1)
    menu = _lunch_and_dinner_menu(
        requirements=requirements, lunch=pre_selected_recipe, dinner=None
    )

    solution = menus.optimise_recipes_for_menu(
        menu=menu, recipes_to_consider=(pre_selected_recipe, other_recipe)
    )

    assert len(solution) == 1
    assert solution[0].recipe_id == other_recipe.id


# Minimum nutrient constraints.

def test_respects_minimum_nutrient_requirement_constraint():
    nutrient = domain_factories.Nutrient()
    minimum_grams = 10

    high_nutrition_recipe = domain_factories.Recipe.any_meal_time_with_nutrient(
        nutrient=nutrient, nutrient_quantity_grams=minimum_grams + 1
    )
    low_nutrition_recipe = domain_factories.Recipe.any_meal_time_with_nutrient(
        nutrient=nutrient, nutrient_quantity_grams=minimum_grams - 1
    )

    menu_item = domain_factories.MenuItem(
        recipe_id=None, meal_time=constants.MealTime.LUNCH
    )
    nutrition_requirement = domain_factories.NutrientRequirement(
        nutrient_id=nutrient.id, minimum_grams=minimum_grams
    )
    menu_requirements = domain_factories.MenuRequirements(
        nutrient_requirements=(nutrition_requirement,)
    )
    menu = domain_factories.Menu(items=[menu_item], requirements=menu_requirements)

    solution = menus.optimise_recipes_for_menu(
        menu=menu,
        recipes_to_consider=(low_nutrition_recipe, high_nutrition_recipe),
    )

    assert len(solution) == 1
    assert solution[0].recipe_id == high_nutrition_recipe.id


def test_respects_minimum_nutrient_requirement_constraint_with_fixed_item():
    nutrient = domain_factories.Nutrient()
    nutrition_requirement = domain_factories.NutrientRequirement(
        nutrient_id=nutrient.id, minimum_grams=10
    )
    lunch_grams = nutrition_requirement.minimum_grams / 2
    min_dinner_grams = nutrition_requirement.minimum_grams - lunch_grams

    # Create two dinner options that can make up the nutrition deficit.
    lunch_recipe = domain_factories.Recipe.any_meal_time_with_nutrient(
        nutrient=nutrient, nutrient_quantity_grams=lunch_grams
    )
    ideal_dinner = domain_factories.Recipe.any_meal_time_with_nutrient(
        nutrient=nutrient, nutrient_quantity_grams=min_dinner_grams + 1
    )
    suboptimal_dinner = domain_factories.Recipe.any_meal_time_with_nutrient(
        nutrient=nutrient, nutrient_quantity_grams=min_dinner_grams - 1
    )

    # Create a menu with lunch already selected.
    menu_requirements = domain_factories.MenuRequirements(
        nutrient_requirements=(nutrition_requirement,),
        maximum_occurrences_per_recipe=1,  # To avoid the lunch recipe getting selected for dinner.
    )
    menu = _lunch_and_dinner_menu(
        requirements=menu_requirements, lunch=lunch_recipe, dinner=None
    )

    solution = menus.optimise_recipes_for_menu(
        menu=menu,
        recipes_to_consider=(lunch_recipe, ideal_dinner, suboptimal_dinner),
    )

    assert len(solution) == 1
    assert solution[0].recipe_id == ideal_dinner.id


# Maximum nutrient constraints.


def test_respects_maximum_nutrient_requirement_constraint():
    nutrient = domain_factories.Nutrient()
    maximum_grams = 10

    # Create two recipes above / below the minimum nutrient requirements.
    low_nutrition_recipe = domain_factories.Recipe.any_meal_time_with_nutrient(
        nutrient=nutrient, nutrient_quantity_grams=maximum_grams - 1
    )
    high_nutrition_recipe = domain_factories.Recipe.any_meal_time_with_nutrient(
        nutrient=nutrient, nutrient_quantity_grams=maximum_grams + 1
    )

    menu_item = domain_factories.MenuItem(
        recipe_id=None, meal_time=constants.MealTime.LUNCH
    )
    nutrition_requirement = domain_factories.NutrientRequirement(
        nutrient_id=nutrient.id, maximum_grams=maximum_grams
    )
    menu_requirements = domain_factories.MenuRequirements(
        nutrient_requirements=(nutrition_requirement,)
    )
    menu = domain_factories.Menu(items=[menu_item], requirements=menu_requirements)

    solution = menus.optimise_recipes_for_menu(
        menu=menu,
        recipes_to_consider=(low_nutrition_recipe, high_nutrition_recipe),
    )

    assert len(solution) == 1
    assert solution[0].recipe_id == low_nutrition_recipe.id


def test_respects_maximum_nutrient_requirement_constraint_with_fixed_item():
    nutrient = domain_factories.Nutrient()
    nutrition_requirement = domain_factories.NutrientRequirement(
        nutrient_id=nutrient.id, maximum_grams=8.3
    )
    lunch_grams = nutrition_requirement.maximum_grams / 2
    max_dinner_grams = nutrition_requirement.maximum_grams - lunch_grams

    # Create two dinner options.
    lunch_recipe = domain_factories.Recipe.any_meal_time_with_nutrient(
        nutrient=nutrient, nutrient_quantity_grams=lunch_grams
    )
    ideal_dinner = domain_factories.Recipe.any_meal_time_with_nutrient(
        nutrient=nutrient, nutrient_quantity_grams=max_dinner_grams - 1
    )
    suboptimal_dinner = domain_factories.Recipe.any_meal_time_with_nutrient(
        nutrient=nutrient, nutrient_quantity_grams=max_dinner_grams + 1
    )

    # Create a menu with lunch already selected.
    menu_requirements = domain_factories.MenuRequirements(
        nutrient_requirements=(nutrition_requirement,),
        maximum_occurrences_per_recipe=1,  # To avoid the lunch recipe getting selected for dinner.
    )
    menu = _lunch_and_dinner_menu(
        requirements=menu_requirements, lunch=lunch_recipe, dinner=None
    )

    solution = menus.optimise_recipes_for_menu(
        menu=menu,
        recipes_to_consider=(lunch_recipe, ideal_dinner, suboptimal_dinner),
    )

    assert len(solution) == 1
    assert solution[0].recipe_id == ideal_dinner.id

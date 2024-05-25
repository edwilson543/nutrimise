import pytest

from nutrimise.app import menus
from tests.factories import data as data_factories


def test_optimises_menu():
    menu = data_factories.Menu()
    menu_requirements = data_factories.MenuRequirements(menu=menu)
    # Create a variety requirement to force the ingredients to be loaded.
    data_factories.VarietyRequirement(menu_requirements=menu_requirements)
    menu_item = data_factories.MenuItem(menu=menu, recipe_id=None)
    recipe = data_factories.Recipe(meal_times=[menu_item.meal_time])

    menus.optimise_menu(menu_id=menu.id)

    menu_item.refresh_from_db()
    assert menu_item.recipe_id == recipe.id


def test_optimises_menu_by_excluding_recipes_not_meeting_dietary_requirements():
    veggie = data_factories.DietaryRequirement()

    menu = data_factories.Menu()
    data_factories.MenuRequirements(menu=menu, dietary_requirements=(veggie,))
    menu_item = data_factories.MenuItem(menu=menu, recipe=None)

    recipe = data_factories.Recipe.create_to_satisfy_dietary_requirements(
        dietary_requirements=(veggie,), meal_times=[menu_item.meal_time]
    )
    data_factories.Recipe(meal_times=[menu_item.meal_time])  # Some non-veggie recipe.

    menus.optimise_menu(menu_id=menu.id)

    menu_item.refresh_from_db()
    assert menu_item.recipe_id == recipe.id


def test_raises_for_menu_without_requirements():
    menu = data_factories.Menu()

    with pytest.raises(menus.MenuHasNoRequirements) as exc:
        menus.optimise_menu(menu_id=menu.id)

    assert exc.value.menu_id == menu.id


def test_raises_if_menu_does_not_exist():
    with pytest.raises(menus.MenuDoesNotExist) as exc:
        menus.optimise_menu(menu_id=123)

    assert exc.value.menu_id == 123

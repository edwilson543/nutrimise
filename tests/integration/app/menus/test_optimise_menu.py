import pytest
from reciply.app import menus

from tests.factories import data as data_factories


def test_optimises_menu():
    menu = data_factories.Menu()
    data_factories.MenuRequirements(menu=menu)
    data_factories.MenuItem(menu=menu)

    menus.optimise_menu(menu_id=menu.id)


def test_raises_for_menu_without_requirements():
    menu = data_factories.Menu()

    with pytest.raises(menus.MenuHasNoRequirements) as exc:
        menus.optimise_menu(menu_id=menu.id)

    assert exc.value.menu_id == menu.id


def test_raises_if_menu_does_not_exist():
    with pytest.raises(menus.MenuDoesNotExist) as exc:
        menus.optimise_menu(menu_id=123)

    assert exc.value.menu_id == 123

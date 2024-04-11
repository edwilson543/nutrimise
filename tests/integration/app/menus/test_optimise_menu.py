# Local application imports
from reciply.app import menus
from tests.factories import data as data_factories


def test_optimises_menu():
    menu = data_factories.Menu()
    data_factories.MenuItem(menu=menu)

    menus.optimise_menu(menu_id=menu.id)

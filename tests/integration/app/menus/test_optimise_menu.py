# Local application imports
from reciply.app import menus
from tests import factories


def test_optimises_menu():
    menu = factories.Menu()
    factories.MenuItem(menu=menu)

    menus.optimise_menu(menu_id=menu.id)

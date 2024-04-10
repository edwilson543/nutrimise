# Third party imports
import pytest

# Local application imports
from reciply.domain import menus
from tests import factories


class TestGetMenu:
    def test_gets_menu_when_exists(self):
        menu = factories.Menu()

        result = menus.get_menu(menu_id=menu.id)

        assert isinstance(result, menus.Menu)
        assert result.id == menu.id

    def test_raises_when_menu_does_not_exist(self):
        with pytest.raises(menus.MenuDoesNotExist) as exc:
            menus.get_menu(menu_id=123)

        assert exc.value.menu_id == 123

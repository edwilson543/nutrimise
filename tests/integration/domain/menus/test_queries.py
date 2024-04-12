import pytest
from reciply.domain import menus

from tests.factories import data as data_factories


class TestGetMenu:
    def test_gets_menu_when_exists(self):
        menu = data_factories.Menu()

        result = menus.get_menu(menu_id=menu.id)

        assert isinstance(result, menus.Menu)
        assert result.id == menu.id

    def test_raises_when_menu_does_not_exist(self):
        with pytest.raises(menus.MenuDoesNotExist) as exc:
            menus.get_menu(menu_id=123)

        assert exc.value.menu_id == 123

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


class TestGetMenusAuthoredByUser:
    def test_gets_menu_authored_by_user(self):
        user = factories.User()
        menu = factories.Menu(author=user)

        other_user = factories.User()
        factories.Menu(author=other_user)

        user_menus = menus.get_menus_authored_by_user(user)

        assert user_menus.get() == menu

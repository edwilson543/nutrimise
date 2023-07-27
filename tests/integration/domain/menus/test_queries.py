# Local application imports
from domain.menus import queries
from tests import factories


class TestGetMenusAuthoredByUser:
    def test_gets_menu_authored_by_user(self):
        user = factories.User()
        menu = factories.Menu(author=user)

        other_user = factories.User()
        factories.Menu(author=other_user)

        user_menus = queries.get_menus_authored_by_user(user)

        assert user_menus.get() == menu

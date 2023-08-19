# Third party imports
import pytest

# Local application imports
from app.menus import _create_menu
from data import constants
from tests import factories


class TestCreateMenu:
    def test_creates_valid_menu(self):
        author = factories.User()

        menu = _create_menu.create_menu(
            author=author,
            name="My menu",
            description="Some description",
        )

        assert menu.author == author
        assert menu.name == "My menu"
        assert menu.description == "Some description"

    def test_creates_menu_with_suggestion_for_each_day_of_week(self):
        user = factories.User()
        for _ in constants.Day.values:
            factories.Recipe(author=user)

        menu = _create_menu.create_menu(
            author=user,
            name="My menu",
            description="Some description",
            add_suggestions=True,
        )

        assert menu.author == user
        assert menu.name == "My menu"
        assert menu.description == "Some description"

        for day in constants.Day.values:
            assert menu.items.get(day=day)

    @pytest.mark.parametrize("name", ["new menu", "NEW Menu"])
    def test_raises_if_user_already_has_menu_with_name(self, name: str):
        author = factories.User()
        factories.Menu(author=author, name="new menu")

        with pytest.raises(_create_menu.MenuNameNotUniqueForAuthor):
            _create_menu.create_menu(
                author=author,
                name=name,
                description="",
            )

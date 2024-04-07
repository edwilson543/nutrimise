# Local application imports
from reciply.app.menus import _add_suggestions_to_menu
from reciply.data import constants
from tests import factories


class TestAddSuggestionsToMenu:
    def test_adds_suggestion_for_each_day_of_week(self):
        user = factories.User()
        menu = factories.Menu(author=user)

        for _ in constants.Day.values:
            factories.Recipe(author=user)

        menu = _add_suggestions_to_menu.add_suggestions_to_menu(menu=menu)

        for day in constants.Day.values:
            assert menu.items.get(day=day)

    def test_creates_menu_with_suggestions_too_few_suggestions_to_fill_a_week(self):
        user = factories.User()
        menu = factories.Menu(author=user)

        available_recipes = 3
        for _ in constants.Day.values[:available_recipes]:
            factories.Recipe(author=user)

        menu = _add_suggestions_to_menu.add_suggestions_to_menu(menu=menu)

        for day in constants.Day.values[:available_recipes]:
            assert menu.items.get(day=day)
        for day in constants.Day.values[available_recipes:]:
            assert not menu.items.filter(day=day).exists()

# Third party imports
import pytest

# Django imports
from django import db as django_db

# Local application imports
from tests.factories import data as data_factories


class TestMenuItemConstraints:
    def test_menu_cannot_have_two_recipes_for_the_same_meal(self):
        menu_item = data_factories.MenuItem()

        with pytest.raises(django_db.IntegrityError):
            data_factories.MenuItem(
                menu=menu_item.menu, meal_time=menu_item.meal_time, day=menu_item.day
            )

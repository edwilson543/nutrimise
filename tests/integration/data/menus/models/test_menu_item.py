# Third party imports
import pytest

# Django imports
from django import db as django_db

# Local application imports
from tests import factories


class TestMenuItemConstraints:
    def test_menu_cannot_have_two_recipes_for_the_same_meal(self):
        menu_item = factories.MenuItem()

        with pytest.raises(django_db.IntegrityError):
            factories.MenuItem(
                menu=menu_item.menu, meal_time=menu_item.meal_time, day=menu_item.day
            )

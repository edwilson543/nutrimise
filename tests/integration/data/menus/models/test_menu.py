# Third party imports
import pytest

# Django imports
from django import db as django_db

# Local application imports
from tests import factories


class TestMenuConstraints:
    def test_user_cannot_have_two_menus_with_the_same_name(self):
        menu = factories.Menu()

        with pytest.raises(django_db.IntegrityError):
            factories.Menu(author=menu.author, name=menu.name)

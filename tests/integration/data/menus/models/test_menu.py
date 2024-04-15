import pytest
from django import db as django_db

from tests.factories import data as data_factories


class TestMenuConstraints:
    def test_user_cannot_have_two_menus_with_the_same_name(self):
        menu = data_factories.Menu()

        with pytest.raises(django_db.IntegrityError):
            data_factories.Menu(author=menu.author, name=menu.name)

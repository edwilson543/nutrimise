# Django imports
from django import db as django_db
from django.contrib.auth import models as auth_models

# Local application imports
from data.menus import models as menu_models

from . import _add_suggestions_to_menu


class MenuNameNotUniqueForAuthor(django_db.IntegrityError):
    pass


def create_menu(
    *,
    author: auth_models.User,
    name: str,
    description: str,
    add_suggestions: bool = False,
) -> menu_models.Menu:
    if menu_models.Menu.objects.filter(name__iexact=name):
        raise MenuNameNotUniqueForAuthor
    menu = menu_models.Menu.new(author=author, name=name, description=description)
    if add_suggestions:
        _add_suggestions_to_menu.add_suggestions_to_menu(menu=menu)
    return menu

import attrs

# Django imports
from django.contrib.auth import models as auth_models
from django.db import models as django_models

# Local application imports
from reciply.data.menus import models as menu_models
from . import _model


@attrs.frozen
class MenuDoesNotExist(Exception):
    menu_id: int


def get_menu(*, menu_id: int) -> _model.Menu:
    try:
        menu = menu_models.Menu.objects.prefetch_related("items").get(id=menu_id)
    except menu_models.Menu.DoesNotExist as exc:
        raise MenuDoesNotExist(menu_id=menu_id) from exc
    return _model.Menu.from_orm_model(menu=menu)


def get_menus_authored_by_user(
    author: auth_models.User,
) -> django_models.QuerySet[menu_models.Menu]:
    return menu_models.Menu.objects.filter(author=author)

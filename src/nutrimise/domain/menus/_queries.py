import attrs

from nutrimise.data.menus import models as menu_models

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

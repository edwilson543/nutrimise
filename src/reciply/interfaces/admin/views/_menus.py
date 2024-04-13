# Standard library imports
from typing import Any

from django import http

from reciply.domain import menus

from . import _base


class MenuDetails(_base.AdminTemplateView):
    template_name = "admin/menus/menu-details.html"

    menu: menus.Menu

    def setup(self, request: http.HttpRequest, *args: object, **kwargs: int) -> None:
        super().setup(request, *args, **kwargs)
        self.menu = menus.get_menu(menu_id=kwargs["menu_id"])

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["menu"] = self.menu
        return context

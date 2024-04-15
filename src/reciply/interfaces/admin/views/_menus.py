# Standard library imports
import collections
from typing import Any

from django import http
from django import urls as django_urls
from django.contrib import messages
from django.views import generic

from reciply.app import menus as menus_app
from reciply.data import constants
from reciply.data.menus import models as menu_models

from . import _base


class MenuDetails(_base.AdminTemplateView):
    template_name = "admin/menus/menu-details.html"

    menu: menu_models.Menu

    def setup(self, request: http.HttpRequest, *args: object, **kwargs: int) -> None:
        super().setup(request, *args, **kwargs)
        self.menu = menu_models.Menu.objects.get(id=kwargs["menu_id"])

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["menu"] = self.menu
        meal_schedule = self.get_meal_schedule()
        context["meal_schedule"] = meal_schedule
        context["days"] = sorted(
            set(day for days in meal_schedule.values() for day in days.keys())
        )
        return context

    def get_meal_schedule(
        self,
    ) -> dict[constants.MealTime, dict[constants.Day, menu_models.MenuItem]]:
        """
        Get the menu items in a way that's easy to construct an HTML table from.
        """
        meal_schedule: dict[
            constants.MealTime, dict[constants.Day, menu_models.MenuItem]
        ] = collections.defaultdict(dict)
        for item in list(self.menu.items.order_by("day")):
            meal_schedule[constants.MealTime(item.meal_time)][
                constants.Day(item.day)
            ] = item
        return dict(meal_schedule)


class OptimiseMenu(generic.View):
    def post(
        self, request: http.HttpRequest, *args: object, **kwargs: int
    ) -> http.HttpResponseRedirect:
        menu_id = kwargs["menu_id"]
        try:
            menus_app.optimise_menu(menu_id=menu_id)
        except menus_app.MenuHasNoRequirements:
            messages.error(request, "The menu has no requirements to optimise against.")
        except menus_app.UnableToOptimiseMenu:
            messages.error(request, "Menu requirements could not be met.")
        else:
            messages.success(request, "Menu has been optimised.")
        redirect_url = django_urls.reverse("menu-details", kwargs={"menu_id": menu_id})
        return http.HttpResponseRedirect(redirect_to=redirect_url)


class LockMenuItemFromOptimiser(generic.View):
    def post(
        self, request: http.HttpRequest, *args: object, **kwargs: int
    ) -> http.HttpResponseRedirect:
        menu_item = menu_models.MenuItem.objects.get(id=kwargs["menu_item_id"])
        menu_item.lock_from_optimiser()
        redirect_url = django_urls.reverse(
            "menu-details", kwargs={"menu_id": menu_item.menu_id}
        )
        return http.HttpResponseRedirect(redirect_to=redirect_url)


class UnlockMenuItemForOptimiser(generic.View):
    def post(
        self, request: http.HttpRequest, *args: object, **kwargs: int
    ) -> http.HttpResponseRedirect:
        menu_item = menu_models.MenuItem.objects.get(id=kwargs["menu_item_id"])
        menu_item.unlock_for_optimiser()
        redirect_url = django_urls.reverse(
            "menu-details", kwargs={"menu_id": menu_item.menu_id}
        )
        return http.HttpResponseRedirect(redirect_to=redirect_url)

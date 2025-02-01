import collections
from typing import Any

from django import http
from django import urls as django_urls
from django.contrib import messages
from django.views import generic

from nutrimise.app import menus as menus_app
from nutrimise.data.ingredients import queries as ingredient_queries
from nutrimise.data.menus import models as menu_models
from nutrimise.domain import constants

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
        context["nutritional_information"] = (
            ingredient_queries.get_nutritional_information_for_menu_per_day(
                menu=self.menu, per_serving=True
            )
        )
        return context

    def get_meal_schedule(
        self,
    ) -> dict[constants.MealTime, dict[int, menu_models.MenuItem]]:
        """
        Get the menu items in a way that's easy to construct an HTML table from.
        """
        meal_schedule: dict[constants.MealTime, dict[int, menu_models.MenuItem]] = (
            collections.defaultdict(dict)
        )
        for item in list(self.menu.items.order_by("day")):
            meal_schedule[constants.MealTime(item.meal_time)][item.day] = item
        ordered_keys = sorted(meal_schedule, key=lambda meal_time: meal_time.order())
        return {key: meal_schedule[key] for key in ordered_keys}


class OptimiseMenu(generic.View):
    def post(
        self, request: http.HttpRequest, *args: object, **kwargs: int
    ) -> http.HttpResponseRedirect:
        menu_id = kwargs["menu_id"]
        try:
            menus_app.optimise_menu(menu_id=menu_id)
        except Exception as exc:
            messages.error(request, str(exc))
        else:
            messages.success(request, "Menu has been optimised.")
        redirect_url = django_urls.reverse("menu-details", kwargs={"menu_id": menu_id})
        return http.HttpResponseRedirect(redirect_to=redirect_url)


class BaseLockUnlockMenuItem(generic.TemplateView):
    template_name = "admin/menus/partials/menu-item.html"
    menu_item: menu_models.MenuItem

    def setup(self, request, *args: object, **kwargs: int):
        super().setup(request, *args, **kwargs)
        self.menu_item = menu_models.MenuItem.objects.get(id=kwargs["menu_item_id"])

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["menu_item"] = self.menu_item
        return context


class LockMenuItemFromOptimiser(BaseLockUnlockMenuItem):
    def post(
        self, request: http.HttpRequest, *args: object, **kwargs: int
    ) -> http.HttpResponse:
        self.menu_item.lock_from_optimiser()
        return super().get(request, *args, **kwargs)


class UnlockMenuItemForOptimiser(BaseLockUnlockMenuItem):
    def post(
        self, request: http.HttpRequest, *args: object, **kwargs: int
    ) -> http.HttpResponse:
        self.menu_item.unlock_for_optimiser()
        return super().get(request, *args, **kwargs)

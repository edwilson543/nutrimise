import collections
from typing import Any

from django import http
from django import urls as django_urls
from django.contrib import messages
from django.views import generic

from nutrimise.app import menus as menus_app
from nutrimise.data.ingredients import queries as ingredient_queries
from nutrimise.data.menus import models as menu_models
from nutrimise.data.menus import operations as menu_operations
from nutrimise.data.recipes import queries as recipe_queries
from nutrimise.domain import embeddings, menus, recipes
from nutrimise.interfaces.admin import forms

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
        context["shopping_list"] = self._get_shopping_list()

        context["optimise_form"] = self._get_optimise_form()
        return context

    def get_meal_schedule(
        self,
    ) -> dict[recipes.MealTime, dict[int, menu_models.MenuItem]]:
        """
        Get the menu items in a way that's easy to construct an HTML table from.
        """
        meal_schedule: dict[recipes.MealTime, dict[int, menu_models.MenuItem]] = (
            collections.defaultdict(dict)
        )
        for item in list(self.menu.items.order_by("day")):
            meal_schedule[recipes.MealTime(item.meal_time)][item.day] = item
        ordered_keys = sorted(meal_schedule, key=lambda meal_time: meal_time.order())
        return {key: meal_schedule[key] for key in ordered_keys}

    def _get_optimise_form(self) -> forms.OptimiseMenu:
        if hasattr(self.menu, "requirements"):
            optimisation_mode = self.menu.requirements.optimisation_mode
        else:
            optimisation_mode = None

        return forms.OptimiseMenu(initial={"optimisation_mode": optimisation_mode})

    def _get_shopping_list(self) -> menus.ShoppingList:
        recipes_ = recipe_queries.get_recipes(recipe_ids=tuple(self.menu.recipe_ids()))
        recipe_lookup = {recipe.id: recipe for recipe in recipes_}

        return menus.get_shopping_list(
            menu=self.menu.to_domain_model(), recipe_lookup=recipe_lookup
        )


class OptimiseMenu(generic.FormView):
    form_class = forms.OptimiseMenu

    def setup(self, request: http.HttpRequest, *args: object, **kwargs: int) -> None:
        super().setup(request, *args, **kwargs)
        self._menu_id = kwargs["menu_id"]

    def form_valid(
        self, form: forms.OptimiseMenu, *args: object, **kwargs: int
    ) -> http.HttpResponse:
        self._embed_prompt(user_prompt=form.cleaned_data.get("prompt"))
        self._update_optimisation_mode(
            optimisation_mode=form.cleaned_data["optimisation_mode"]
        )

        try:
            menus_app.optimise_menu(menu_id=self._menu_id)
        except Exception as exc:
            messages.error(self.request, str(exc))
        else:
            messages.success(self.request, "Menu has been optimised.")
        return super().form_valid(form=form)

    def _embed_prompt(self, user_prompt: str | None) -> None:
        if not user_prompt:
            return

        embedding_service = embeddings.get_embedding_service()
        menus_app.create_or_update_menu_embedding(
            menu_id=self._menu_id,
            embedding_service=embedding_service,
            user_prompt=user_prompt,
        )

    def _update_optimisation_mode(self, optimisation_mode: str) -> None:
        menu_operations.update_menu_requirements(
            menu_id=self._menu_id,
            optimisation_mode=menus.OptimisationMode(optimisation_mode),
        )

    def get_success_url(self) -> str:
        return django_urls.reverse("menu-details", kwargs={"menu_id": self._menu_id})


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

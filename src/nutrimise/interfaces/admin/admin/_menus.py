from typing import Any

from django import forms as django_forms
from django import http
from django import urls as django_urls
from django.contrib import admin
from django.utils import safestring

from nutrimise.app import menus as menus_app
from nutrimise.data.menus import models as menu_models
from nutrimise.domain import embeddings, menus, recipes


class _MenuRequirementsInline(admin.StackedInline):
    model = menu_models.MenuRequirements
    show_change_link = True


class _MenuItemInline(admin.TabularInline):
    model = menu_models.MenuItem

    list_display = ["id", "menu", "recipe", "format_day", "meal_time"]
    ordering = ["menu", "day", "meal_time"]
    search_fields = ["menu"]

    @admin.display()
    def format_day(self, menu_item: menu_models.MenuItem) -> str:
        return f"Day {menu_item.day}"


class _MenuChangeForm(django_forms.ModelForm):
    number_of_days = django_forms.IntegerField(min_value=1)
    meal_times = django_forms.MultipleChoiceField(choices=recipes.MealTime.choices)

    class Meta:
        model = menu_models.Menu
        fields = ["author", "name", "description"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if menu := kwargs.get("instance"):
            initial_days: set[int] = set()
            initial_meal_times: set[str] = set()
            for item in list(menu.items.values("day", "meal_time")):
                initial_days.add(item["day"])
                initial_meal_times.add(item["meal_time"])
            self.fields["number_of_days"].initial = len(initial_days)
            self.fields["meal_times"].initial = list(initial_meal_times)


@admin.register(menu_models.Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name_",
        "author",
        "meals",
        "dietary_requirements",
        "user_actions",
    ]
    list_display_links = ["name_"]
    ordering = ["name"]
    search_fields = ["name"]

    form = _MenuChangeForm

    inlines = [_MenuRequirementsInline, _MenuItemInline]

    @admin.display(description="Name")
    def name_(self, menu: menu_models.Menu) -> safestring.SafeString:
        detail_url = django_urls.reverse("menu-details", kwargs={"menu_id": menu.id})
        return safestring.mark_safe(f'<a href="{detail_url}"><b>{menu.name}</b></a>')

    @admin.display(description="Actions")
    def user_actions(self, menu: menu_models.Menu) -> safestring.SafeString:
        detail_url = django_urls.reverse("menu-details", kwargs={"menu_id": menu.id})
        edit_url = django_urls.reverse(
            "admin:menus_menu_change", kwargs={"object_id": menu.id}
        )
        return safestring.mark_safe(
            f'<a href="{detail_url}"><b>Optimise</b></a> | <a href="{edit_url}"><b>Edit</b></a>'
        )

    @admin.display()
    def meals(self, menu: menu_models.Menu) -> int:
        return menu.items.count()

    @admin.display()
    def dietary_requirements(self, menu: menu_models.Menu) -> int:
        if not menu.requirements:
            return 0
        return menu.requirements.dietary_requirements.count()

    def save_model(
        self,
        request: http.HttpRequest,
        obj: menu_models.Menu,
        form: _MenuChangeForm,
        change: bool,
    ) -> None:
        """
        Create the menu with the specified menu item schedule.
        """
        super().save_model(request=request, obj=obj, form=form, change=change)
        number_of_days = form.cleaned_data["number_of_days"]
        meal_times = form.cleaned_data["meal_times"]
        if change:
            for menu_item in obj.items.all():
                valid_day = menu_item.day <= number_of_days
                valid_meal_time = menu_item.meal_time in meal_times
                if not (valid_day and valid_meal_time):
                    menu_item.delete()

        for day in range(1, number_of_days + 1):
            for meal_time in meal_times:
                obj.items.get_or_create(day=day, meal_time=meal_time)

        if obj.requirements.optimisation_mode == menus.OptimisationMode.SEMANTIC:
            menus_app.create_or_update_menu_embedding(
                menu_id=obj.id, embedding_service=embeddings.get_embedding_service()
            )


@admin.register(menu_models.MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ["id", "menu", "recipe", "format_day", "meal_time"]
    ordering = ["menu", "day", "meal_time"]
    search_fields = ["menu"]

    @admin.display()
    def format_day(self, menu_item: menu_models.MenuItem) -> str:
        return f"Day {menu_item.day}"


class _NutrientRequirementInline(admin.TabularInline):
    model = menu_models.NutrientRequirement


class _VarietyRequirementInline(admin.TabularInline):
    model = menu_models.VarietyRequirement


@admin.register(menu_models.MenuRequirements)
class MenuRequirementsAdmin(admin.ModelAdmin):
    list_display = ["requirements", "menu_details"]
    list_display_links = ["requirements"]
    inlines = [_NutrientRequirementInline, _VarietyRequirementInline]

    @admin.display(description="Requirements")
    def requirements(self, menu_requirements: menu_models.MenuRequirements) -> str:
        return str(menu_requirements)

    @admin.display(description="Menu")
    def menu_details(
        self, menu_requirements: menu_models.MenuRequirements
    ) -> safestring.SafeString:
        menu = menu_requirements.menu
        menu_url = django_urls.reverse("menu-details", kwargs={"menu_id": menu.id})
        return safestring.mark_safe(f'<a href="{menu_url}">{menu.name}</a>')


@admin.register(menu_models.MenuEmbedding)
class MenuEmbeddingAdmin(admin.ModelAdmin):
    list_display = [
        "vendor",
        "model",
        "prompt_hash",
        "vector_length",
        "menu_name",
    ]
    list_display_links = ["prompt_hash"]
    ordering = ["menu__name"]

    @admin.display(description="Menu name")
    def menu_name(self, embedding: menu_models.MenuEmbedding) -> str:
        return embedding.menu.name

    @admin.display(description="Vector length")
    def vector_length(self, embedding: menu_models.MenuEmbedding) -> int:
        return len(embedding.vector)

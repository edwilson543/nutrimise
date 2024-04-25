from typing import Any

from django import forms, http
from django import urls as django_urls
from django.contrib import admin
from django.utils import safestring

from nutrimise.data import constants
from nutrimise.data.menus import models as menu_models


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
        return constants.Day(int(menu_item.day)).label.title()


class _MenuChangeForm(forms.ModelForm):
    days = forms.MultipleChoiceField(choices=constants.Day.choices)
    meal_times = forms.MultipleChoiceField(choices=constants.MealTime.choices)

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
            self.fields["days"].initial = list(initial_days)
            self.fields["meal_times"].initial = list(initial_meal_times)


@admin.register(menu_models.Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "author",
        "meals",
        "dietary_requirements",
        "user_actions",
    ]
    ordering = ["name"]
    search_fields = ["name"]

    form = _MenuChangeForm

    inlines = [_MenuRequirementsInline, _MenuItemInline]

    @admin.display(description="Actions")
    def user_actions(self, menu: menu_models.Menu) -> safestring.SafeString:
        detail_url = django_urls.reverse("menu-details", kwargs={"menu_id": menu.id})
        edit_url = django_urls.reverse(
            "admin:menus_menu_change", kwargs={"object_id": menu.id}
        )
        return safestring.mark_safe(
            f'<a href="{detail_url}"><b>View</b></a> | <a href="{edit_url}"><b>Edit</b></a>'
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
        days = form.cleaned_data["days"]
        meal_times = form.cleaned_data["meal_times"]
        if change:
            for menu_item in obj.items.all():
                valid_day = menu_item.day in days
                valid_meal_time = menu_item.meal_time in meal_times
                if not (valid_day and valid_meal_time):
                    menu_item.delete()

        for day in days:
            for meal_time in meal_times:
                obj.items.get_or_create(day=day, meal_time=meal_time)


@admin.register(menu_models.MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ["id", "menu", "recipe", "format_day", "meal_time"]
    ordering = ["menu", "day", "meal_time"]
    search_fields = ["menu"]

    @admin.display()
    def format_day(self, menu_item: menu_models.MenuItem) -> str:
        return constants.Day(int(menu_item.day)).label.title()


class _NutrientRequirementInline(admin.TabularInline):
    model = menu_models.NutrientRequirement


class _VarietyRequirementInline(admin.TabularInline):
    model = menu_models.VarietyRequirement


@admin.register(menu_models.MenuRequirements)
class MenuRequirementsAdmin(admin.ModelAdmin):
    inlines = [_NutrientRequirementInline, _VarietyRequirementInline]

from django import forms, http
from django import urls as django_urls
from django.contrib import admin
from django.utils import safestring

from reciply.data import constants
from reciply.data.ingredients import models as ingredient_models
from reciply.data.menus import models as menu_models
from reciply.data.recipes import models as recipe_models

admin.site.site_header = "Reciply admin"
admin.site.site_title = "Reciply"

# ----------
# Recipes
# ----------


@admin.register(recipe_models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "author", "user_actions"]
    ordering = ["name"]
    search_fields = ["name"]

    @admin.display(description="Actions")
    def user_actions(self, recipe: recipe_models.Recipe) -> safestring.SafeString:
        detail_url = django_urls.reverse(
            "recipe-details", kwargs={"recipe_id": recipe.id}
        )
        edit_url = django_urls.reverse(
            "admin:recipes_recipe_change", kwargs={"object_id": recipe.id}
        )
        return safestring.mark_safe(
            f'<a href="{detail_url}"><b>View</b></a> | <a href="{edit_url}"><b>Edit</b></a>'
        )


@admin.register(recipe_models.RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ["id", "recipe_name", "ingredient_name", "quantity", "units"]
    ordering = ["recipe__name", "ingredient__name_singular"]

    @admin.display(description="Recipe name")
    def recipe_name(self, ingredient: recipe_models.RecipeIngredient) -> str:
        return ingredient.recipe.name

    @admin.display(description="Ingredient name")
    def ingredient_name(self, ingredient: recipe_models.RecipeIngredient) -> str:
        return ingredient.ingredient.name_singular

    @admin.display(description="Units")
    def units(self, ingredient: recipe_models.RecipeIngredient) -> str:
        return ingredient.ingredient.units or "No units"


# ----------
# Menus
# ----------


@admin.register(menu_models.Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "author", "meals", "user_actions"]
    ordering = ["name"]
    search_fields = ["name"]

    class CreateForm(forms.ModelForm):
        days = forms.MultipleChoiceField(choices=constants.Day.choices)
        meal_times = forms.MultipleChoiceField(choices=constants.MealTime.choices)

        class Meta:
            model = menu_models.Menu
            fields = ["author", "name", "description"]

    form = CreateForm

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

    def save_model(
        self,
        request: http.HttpRequest,
        obj: menu_models.Menu,
        form: CreateForm,
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


# ----------
# Ingredients
# ----------


@admin.register(ingredient_models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "units"]
    ordering = ["name_singular"]

    @admin.display(description="Name")
    def name(self, ingredient: ingredient_models.Ingredient) -> str:
        return ingredient.name_singular

    @admin.display(description="Units")
    def units(self, ingredient: ingredient_models.Ingredient) -> str:
        return ingredient.units or "-"


@admin.register(ingredient_models.Nutrient)
class NutrientAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    ordering = ["name"]


@admin.register(ingredient_models.IngredientNutritionalInformation)
class IngredientNutritionalInformationAdmin(admin.ModelAdmin):
    list_display = ["id", "ingredient_name", "nutrient_name", "quantity_per_gram"]
    ordering = ["ingredient__name_singular"]

    @admin.display(description="Ingredient")
    def ingredient_name(
        self,
        nutritional_information: ingredient_models.IngredientNutritionalInformation,
    ) -> str:
        return nutritional_information.ingredient.name_singular

    @admin.display(description="Nutrient")
    def nutrient_name(
        self,
        nutritional_information: ingredient_models.IngredientNutritionalInformation,
    ) -> str:
        return nutritional_information.nutrient.name

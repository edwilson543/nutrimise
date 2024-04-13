import factory
from reciply.data import constants
from reciply.data.menus import models as menu_models

from . import _auth, _ingredients, _recipes


class Menu(factory.django.DjangoModelFactory):
    author = factory.SubFactory(_auth.User)
    name = factory.Sequence(lambda n: f"menu-{n}")
    description = "Some description"

    class Meta:
        model = menu_models.Menu


class MenuItem(factory.django.DjangoModelFactory):
    menu = factory.SubFactory(Menu)
    recipe = factory.SubFactory(_recipes.Recipe)
    meal_time = constants.MealTime.LUNCH
    day = constants.Day.MONDAY

    class Meta:
        model = menu_models.MenuItem


class MenuRequirements(factory.django.DjangoModelFactory):
    maximum_occurrences_per_recipe = 1

    class Meta:
        model = menu_models.MenuRequirements


class NutrientRequirement(factory.django.DjangoModelFactory):
    nutrient = factory.SubFactory(_ingredients.Nutrient)
    minimum_grams = None
    maximum_grams = None
    target_grams = None
    enforcement_interval = constants.NutrientRequirementEnforcementInterval.DAILY

    class Meta:
        model = menu_models.NutrientRequirement

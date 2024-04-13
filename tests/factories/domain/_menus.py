import factory
from reciply.data import constants
from reciply.data.menus import models as menu_models
from reciply.domain import menus


class MenuItem(factory.Factory):
    id = factory.Sequence(lambda n: n)
    recipe_id = None
    day = constants.Day.MONDAY
    meal_time = constants.MealTime.LUNCH
    optimiser_generated = True

    class Meta:
        model = menus.MenuItem


class MenuRequirements(factory.Factory):
    nutrient_requirements = factory.LazyFunction(tuple)
    maximum_occurrences_per_recipe = 1

    class Meta:
        model = menus.MenuRequirements


class Menu(factory.Factory):
    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f"menu-{n}")
    description = "Some description"
    items = factory.LazyFunction(tuple)
    requirements = factory.SubFactory(MenuRequirements)

    class Meta:
        model = menus.Menu


class NutrientRequirement(factory.Factory):
    nutrient_id = factory.Sequence(lambda n: n)
    minimum_grams = None
    maximum_grams = None
    target_grams = None
    enforcement_interval = menu_models.NutrientRequirementEnforcementInterval.DAILY

    class Meta:
        model = menus.NutrientRequirement

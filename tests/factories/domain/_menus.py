# Third party imports
import factory

# Local application imports
from reciply.data import constants
from reciply.data.menus import models as menu_models
from reciply.domain import menus


class Menu(factory.Factory):
    id = factory.Sequence(lambda n: n)
    items = factory.LazyFunction(tuple)
    requirements = factory.LazyFunction(tuple)

    class Meta:
        model = menus.Menu


class MenuItem(factory.Factory):
    id = factory.Sequence(lambda n: n)
    recipe_id = None
    day = constants.Day.MONDAY
    meal_time = constants.MealTime.LUNCH
    optimiser_generated = False

    class Meta:
        model = menus.MenuItem


class MenuRequirements(factory.Factory):
    nutrient_requirements = factory.LazyFunction(tuple)
    maximum_occurrences_per_recipe = 1

    class Meta:
        model = menus.MenuRequirements


class NutrientRequirements(factory.Factory):
    nutrient_id = factory.Sequence(lambda n: n)
    minimum_grams = None
    maximum_grams = None
    target_grams = None
    enforcement_interval = menu_models.NutrientRequirementEnforcementInterval.DAILY

    class Meta:
        model = menus.NutrientRequirement

import factory

from nutrimise.data import constants
from nutrimise.domain import menus


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
    variety_requirements = factory.LazyFunction(tuple)
    maximum_occurrences_per_recipe = 1
    dietary_requirement_ids = factory.LazyFunction(tuple)

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
    minimum_quantity = None
    maximum_quantity = None
    target_quantity = None
    units = constants.NutrientUnit.GRAMS
    enforcement_interval = constants.NutrientRequirementEnforcementInterval.DAILY

    class Meta:
        model = menus.NutrientRequirement


class VarietyRequirement(factory.Factory):
    ingredient_category_id = factory.Sequence(lambda n: n)
    minimum = None
    maximum = None
    target = None

    class Meta:
        model = menus.VarietyRequirement

import factory

from nutrimise.data.ingredients import models as ingredient_models
from nutrimise.data.menus import models as menu_models
from nutrimise.domain import constants, menus

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
    day = factory.Sequence(lambda n: n + 1)

    class Meta:
        model = menu_models.MenuItem


class MenuRequirements(factory.django.DjangoModelFactory):
    optimisation_mode = menus.OptimisationMode.RANDOM.value
    maximum_occurrences_per_recipe = 1

    class Meta:
        model = menu_models.MenuRequirements
        skip_postgeneration_save = True

    @factory.post_generation
    def dietary_requirements(
        obj,
        create: bool,
        extracted: tuple[ingredient_models.DietaryRequirement, ...],
        **kwargs: object,
    ):
        if not create:
            return
        elif extracted:
            obj.dietary_requirements.add(*extracted)


class NutrientRequirement(factory.django.DjangoModelFactory):
    nutrient = factory.SubFactory(_ingredients.Nutrient)
    minimum_quantity = None
    maximum_quantity = None
    target_quantity = None
    units = constants.NutrientUnit.GRAMS
    enforcement_interval = constants.NutrientRequirementEnforcementInterval.DAILY

    class Meta:
        model = menu_models.NutrientRequirement


class VarietyRequirement(factory.django.DjangoModelFactory):
    ingredient_category = factory.SubFactory(_ingredients.IngredientCategory)
    minimum = None
    maximum = None
    target = None

    class Meta:
        model = menu_models.VarietyRequirement

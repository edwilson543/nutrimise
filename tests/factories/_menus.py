# Third party imports
import factory

# Local application imports
from reciply.data import constants
from reciply.data.menus import models as menu_models

from . import _auth, _recipes


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

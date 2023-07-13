# Third party imports
import factory

# Local application imports
from data.recipes import models as recipe_models

from . import _auth


class Recipe(factory.django.DjangoModelFactory):
    author = factory.SubFactory(_auth.User)
    name = factory.Sequence(lambda n: f"recipe-{n}")
    description = "Some description"

    class Meta:
        model = recipe_models.Recipe

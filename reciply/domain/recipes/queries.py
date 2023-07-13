# Django imports
from django.contrib.auth import models as auth_models
from django.db import models as django_models

# Local application imports
from data.recipes import models as recipe_models


def get_recipes_authored_by_user(
    author: auth_models.User,
) -> django_models.QuerySet[recipe_models.Recipe]:
    return recipe_models.Recipe.objects.filter(author=author)

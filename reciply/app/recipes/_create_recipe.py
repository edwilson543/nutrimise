# Django imports
from django import db as django_db
from django.contrib.auth import models as auth_models

# Local application imports
from data.recipes import models as recipe_models


class RecipeNameNotUniqueForAuthor(django_db.IntegrityError):
    pass


def create_recipe(
    author: auth_models.User, name: str, description: str
) -> recipe_models.Recipe:
    try:
        return recipe_models.Recipe.new(
            author=author, name=name, description=description
        )
    except django_db.IntegrityError:
        raise RecipeNameNotUniqueForAuthor

# Django imports
from django import db as django_db
from django.contrib.auth import models as auth_models
from django.core import files
from django.db import transaction

# Local application imports
from data.recipes import models as recipe_models

from . import _create_recipe_image


class RecipeNameNotUniqueForAuthor(django_db.IntegrityError):
    pass


def create_recipe(
    author: auth_models.User, name: str, description: str, hero_image: files.File | None
) -> recipe_models.Recipe:
    if recipe_models.Recipe.objects.filter(name__iexact=name):
        raise RecipeNameNotUniqueForAuthor

    with transaction.atomic():
        recipe = recipe_models.Recipe.new(
            author=author, name=name, description=description
        )
        if hero_image:
            _create_recipe_image.create_recipe_image(
                recipe=recipe, is_hero=True, file=hero_image.file
            )
    return recipe

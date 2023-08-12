# Standard library imports
import io

# Django imports
from django import db as django_db

# Local application imports
from data.recipes import models as recipe_models
from domain import storage


class RecipeAlreadyHasHeroImage(django_db.IntegrityError):
    pass


def create_recipe_image(
    *, recipe: recipe_models.Recipe, is_hero: bool, file: io.BytesIO
) -> recipe_models.RecipeImage:
    store = storage.get_file_storage()
    storage_context = store.context_class.for_recipe(recipe=recipe)

    try:
        recipe_image = recipe.new_image(
            is_hero=is_hero, storage_context=storage_context.serialize()
        )
    except django_db.IntegrityError:
        raise RecipeAlreadyHasHeroImage

    store.upload(file=file, storage_context=storage_context)

    return recipe_image

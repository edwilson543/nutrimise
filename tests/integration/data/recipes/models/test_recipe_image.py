# Third party imports
import pytest

# Django imports
from django import db as django_db

# Local application imports
from tests import factories


class TestRecipeImage:
    def test_cannot_create_two_hero_images_for_one_recipe(self):
        image = factories.RecipeImage(is_hero=True)

        with pytest.raises(django_db.IntegrityError):
            factories.RecipeImage(recipe=image.recipe, is_hero=True)

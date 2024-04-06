# Third party imports
import pytest

# Django imports
from django import db as django_db

# Local application imports
from tests import factories


class TestIngredientFeaturesMaxOncePerRecipe:
    def test_attempt_to_violate_constraint_raises(self):
        recipe_ingredient = factories.RecipeIngredient()

        with pytest.raises(django_db.IntegrityError):
            factories.RecipeIngredient(
                recipe=recipe_ingredient.recipe, ingredient=recipe_ingredient.ingredient
            )

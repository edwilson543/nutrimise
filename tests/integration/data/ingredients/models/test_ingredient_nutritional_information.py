# Third party imports
import pytest

# Django imports
from django import db as django_db

# Local application imports
from tests import factories


class TestIngredientNutrientUniqueTogetherConstraint:
    def test_attempt_to_violate_constraint_raises(self):
        nutritional_information = factories.IngredientNutritionalInformation()

        with pytest.raises(django_db.IntegrityError):
            factories.IngredientNutritionalInformation(
                ingredient=nutritional_information.ingredient,
                nutrient=nutritional_information.nutrient,
            )

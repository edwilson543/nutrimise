import pytest

from django import db as django_db

from tests.factories import data as data_factories


class TestIngredientNutrientUniqueTogetherConstraint:
    def test_attempt_to_violate_constraint_raises(self):
        nutritional_information = data_factories.IngredientNutritionalInformation()

        with pytest.raises(django_db.IntegrityError):
            data_factories.IngredientNutritionalInformation(
                ingredient=nutritional_information.ingredient,
                nutrient=nutritional_information.nutrient,
            )

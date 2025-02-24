from django.core import management as django_management
from django.test import override_settings

from testing.factories import data as data_factories


@override_settings(IMAGE_EXTRACTION_VENDOR="FAKE")
def test_gathers_ingredient_nutritional_information():
    ingredient = data_factories.Ingredient()
    nutrient = data_factories.Nutrient()

    django_management.call_command("gather_ingredient_nutritional_information")

    nutritional_info = ingredient.nutritional_information.get()
    assert nutritional_info.nutrient_id == nutrient.id

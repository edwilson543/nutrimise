from nutrimise.app import ingredients as ingredients_app
from nutrimise.domain.image_extraction import _vendors as image_extraction_vendors
from testing.factories import data as data_factories


def test_gathers_nutritional_information_for_all_ingredients():
    ingredient = data_factories.Ingredient()
    other_ingredient = data_factories.Ingredient()

    nutrient = data_factories.Nutrient()
    other_nutrient = data_factories.Nutrient()

    extraction_service = image_extraction_vendors.FakeImageExtractionService()

    ingredients_app.gather_ingredient_nutritional_information(
        extraction_service=extraction_service
    )

    for ingredient_ in [ingredient, other_ingredient]:
        assert ingredient_.nutritional_information.count() == 2
        assert ingredient_.nutritional_information.get(nutrient_id=nutrient.id)
        assert ingredient_.nutritional_information.get(nutrient_id=other_nutrient.id)


def test_skips_gathering_nutritional_information_for_ingredient_with_info():
    ingredient_without_info = data_factories.Ingredient()

    ingredient = data_factories.Ingredient()
    nutrient = data_factories.Nutrient()
    data_factories.IngredientNutritionalInformation(
        ingredient=ingredient, nutrient=nutrient, quantity_per_gram=39.1
    )

    extraction_service = image_extraction_vendors.FakeImageExtractionService()

    ingredients_app.gather_ingredient_nutritional_information(
        extraction_service=extraction_service
    )

    ingredient_nutritional_info = ingredient.nutritional_information.get()
    assert ingredient_nutritional_info.quantity_per_gram == 39.1

    other_ing_nutritional_info = ingredient_without_info.nutritional_information.get()
    assert other_ing_nutritional_info.quantity_per_gram == 1.0

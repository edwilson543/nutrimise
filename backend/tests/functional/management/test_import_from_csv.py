from django.core import management as django_management

from nutrimise.data.ingredients import models as ingredient_models
from nutrimise.domain import ingredients


def test_example_dataset_can_be_imported():
    django_management.call_command("import_from_csv", dataset="test")

    assert ingredient_models.DietaryRequirement.objects.count() == 2

    nutrient = ingredient_models.Nutrient.objects.get()
    assert nutrient.name == "Protein"
    assert nutrient.category == ingredients.NutrientCategory.MACRO
    assert nutrient.units == ingredients.NutrientUnit.GRAMS

    ingredient_category = ingredient_models.IngredientCategory.objects.get()
    assert ingredient_category.name == "Vegetable"

    ingredient = ingredient_models.Ingredient.objects.get()
    assert ingredient.name == "Carrot"
    assert ingredient.category == ingredient_category
    assert ingredient.units == "GRAMS"
    assert ingredient.grams_per_unit == 1.0
    assert ingredient.dietary_requirements_satisfied.count() == 2

    nutritional_information = (
        ingredient_models.IngredientNutritionalInformation.objects.get()
    )
    assert nutritional_information.ingredient == ingredient
    assert nutritional_information.nutrient == nutrient
    assert nutritional_information.quantity_per_gram == 0.03

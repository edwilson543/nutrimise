import pytest

from nutrimise.data.ingredients import models as ingredient_models
from nutrimise.data.ingredients import operations as ingredient_operations
from testing.factories import data as data_factories


class TestGetOrCreateIngredientCategory:
    def test_creates_category_with_name(self):
        name = "Protein"

        category = ingredient_operations.get_or_create_ingredient_category(name=name)

        persisted_category = ingredient_models.IngredientCategory.objects.get()
        assert category.id == persisted_category.id
        assert category.name == name

    @pytest.mark.parametrize("name", ["protein", "Protein", "PROTEIN"])
    def test_gets_existing_ingredient_category_matching_name(self, name: str):
        existing_category = data_factories.IngredientCategory(name=name.lower())

        ingredient_operations.get_or_create_ingredient_category(name=name)

        assert ingredient_models.IngredientCategory.objects.get() == existing_category


class TestGetOrCreateIngredient:
    def test_creates_ingredient_with_name(self):
        category = data_factories.IngredientCategory()
        name = "Chicken"

        ingredient = ingredient_operations.get_or_create_ingredient(
            name=name, category_id=category.id, units="Grams", grams_per_unit=1.0
        )

        persisted_ingredient = ingredient_models.Ingredient.objects.get()
        assert ingredient.id == persisted_ingredient.id
        assert ingredient.name == persisted_ingredient.name == name
        assert ingredient.category.id == category.id
        assert ingredient.units == "Grams"
        assert ingredient.grams_per_unit == 1.0

    @pytest.mark.parametrize("name", ["brocoli", "Brocoli", "BROCOLI"])
    def test_gets_existing_ingredient_matching_name(self, name: str):
        existing_ingredient = data_factories.Ingredient.create(name=name.lower())

        result = ingredient_operations.get_or_create_ingredient(
            name=name,
            category_id=existing_ingredient.category_id,
            units="Something random",
            grams_per_unit=existing_ingredient.grams_per_unit,
        )

        assert ingredient_models.Ingredient.objects.get() == existing_ingredient
        assert existing_ingredient.to_domain_model() == result

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

    def test_gets_existing_category_matching_name(self):
        existing_category = data_factories.IngredientCategory()

        ingredient_operations.get_or_create_ingredient_category(
            name=existing_category.name
        )

        assert ingredient_models.IngredientCategory.objects.get() == existing_category

    def test_gets_existing_category_matching_name_case_insensitively(self):
        existing_category = data_factories.IngredientCategory(name="Protein")

        ingredient_operations.get_or_create_ingredient_category(name="PROTEIN")

        assert ingredient_models.IngredientCategory.objects.get() == existing_category

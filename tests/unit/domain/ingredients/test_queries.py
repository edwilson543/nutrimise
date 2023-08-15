# Local application imports
from domain.ingredients import queries
from tests import factories


class TestGetIngredientDisplayName:
    def test_plural_with_units(self):
        ingredient = factories.Ingredient.build(
            name_singular="chicken", name_plural="chickens", units="g"
        )

        displayed_name = queries.get_ingredient_display_name(
            ingredient=ingredient, quantity=0.57821
        )

        assert displayed_name == "0.58 g of chicken"

    def test_singular_with_units(self):
        ingredient = factories.Ingredient.build(
            name_singular="chicken", name_plural="chickens", units="g"
        )

        displayed_name = queries.get_ingredient_display_name(
            ingredient=ingredient, quantity=1
        )

        assert displayed_name == "1 g of chicken"

    def test_plural_without_units(self):
        ingredient = factories.Ingredient.build(
            name_singular="apple", name_plural="apples"
        )

        displayed_name = queries.get_ingredient_display_name(
            ingredient=ingredient, quantity=1
        )

        assert displayed_name == "1 apple"

    def test_singular_without_units(self):
        ingredient = factories.Ingredient.build(
            name_singular="apple", name_plural="apples"
        )

        displayed_name = queries.get_ingredient_display_name(
            ingredient=ingredient, quantity=2
        )

        assert displayed_name == "2 apples"

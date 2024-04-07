# Third party imports
import pytest

# Local application imports
from reciply.domain.ingredients import queries
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

    @pytest.mark.parametrize("quantity", [1, 1.0])
    def test_plural_without_units(self, quantity: int | float):
        ingredient = factories.Ingredient.build(
            name_singular="apple", name_plural="apples", units=None
        )

        displayed_name = queries.get_ingredient_display_name(
            ingredient=ingredient, quantity=quantity
        )

        assert displayed_name == "1 apple"

    @pytest.mark.parametrize("quantity", [2, 2.0])
    def test_singular_without_units(self, quantity: int | float):
        ingredient = factories.Ingredient.build(
            name_singular="apple", name_plural="apples", units=None
        )

        displayed_name = queries.get_ingredient_display_name(
            ingredient=ingredient, quantity=quantity
        )

        assert displayed_name == "2 apples"

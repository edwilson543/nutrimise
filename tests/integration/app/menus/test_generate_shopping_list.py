# Local application imports
from app.menus import _generate_shopping_list
from data import constants
from tests import factories


class TestGenerateShoppingList:
    def test_aggregates_same_ingredient_from_different_recipes(self):
        menu = factories.Menu()

        apple = factories.Ingredient(
            name_singular="apple", name_plural="apples", category="Fruit", units=None
        )
        recipe_a = factories.Recipe()
        factories.RecipeIngredient(recipe=recipe_a, ingredient=apple, quantity=1)
        factories.MenuItem(recipe=recipe_a, menu=menu, day=constants.Day.MONDAY)

        recipe_b = factories.Recipe()
        factories.RecipeIngredient(recipe=recipe_b, ingredient=apple, quantity=1)
        factories.MenuItem(recipe=recipe_b, menu=menu, day=constants.Day.TUESDAY)

        list_ = _generate_shopping_list.generate_shopping_list(menu=menu)

        assert len(list_.keys()) == 1

        fruit_list = list_["Fruit"]
        assert len(fruit_list) == 1
        assert fruit_list[0] == "2 apples"

    def test_splits_list_into_categories(self):
        menu = factories.Menu()

        apple = factories.Ingredient(
            name_singular="apple", name_plural="apples", category="Fruit", units=None
        )
        apple_recipe = factories.Recipe()
        factories.RecipeIngredient(recipe=apple_recipe, ingredient=apple, quantity=1)
        factories.MenuItem(recipe=apple_recipe, menu=menu, day=constants.Day.MONDAY)

        chicken_breast = factories.Ingredient(
            name_singular="chicken breast", category="Meat", units="g"
        )
        chicken_recipe = factories.Recipe()
        factories.RecipeIngredient(
            recipe=chicken_recipe, ingredient=chicken_breast, quantity=100
        )
        factories.MenuItem(recipe=chicken_recipe, menu=menu, day=constants.Day.TUESDAY)

        list_ = _generate_shopping_list.generate_shopping_list(menu=menu)

        assert len(list_.keys()) == 2

        fruit_list = list_["Fruit"]
        assert len(fruit_list) == 1
        assert fruit_list[0] == "1 apple"

        meat_list = list_["Meat"]
        assert len(meat_list) == 1
        assert meat_list[0] == "100 g of chicken breast"

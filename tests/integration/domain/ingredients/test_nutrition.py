# Local application imports
from data import constants
from domain.ingredients import nutrition
from tests import factories


class TestNutritionalInformation:
    def test_for_ingredient_gets_correct_nutritional_information(self):
        apple = factories.Ingredient.build(
            name_singular="apple",
            grams_per_unit=200,
            protein_per_gram=0.1,
            carbohydrates_per_gram=0.3,
        )

        nutritional_information = nutrition.NutritionalInformation.for_ingredient(
            ingredient=apple, quantity=2
        )

        assert nutritional_information.protein_grams == 40
        assert nutritional_information.carbohydrates_grams == 120

    def test_for_recipe_gets_correct_nutritional_information(self):
        apple = factories.Ingredient(
            name_singular="apple",
            grams_per_unit=200,
            protein_per_gram=0.1,
            carbohydrates_per_gram=0.3,
        )
        crumble = factories.Ingredient(
            name_singular="crumble",
            grams_per_unit=1,
            units="g",
            protein_per_gram=0.05,
            carbohydrates_per_gram=0.65,
        )

        recipe = factories.Recipe()
        factories.RecipeIngredient(recipe=recipe, ingredient=apple, quantity=4)
        factories.RecipeIngredient(recipe=recipe, ingredient=crumble, quantity=500)

        nutritional_information = nutrition.NutritionalInformation.for_recipe(
            recipe=recipe
        )

        assert nutritional_information.protein_grams == 105
        assert nutritional_information.carbohydrates_grams == 565

    def test_for_recipe_returns_zero_nutritional_information_when_has_no_ingredients(
        self,
    ):
        recipe = factories.Recipe()

        nutritional_information = nutrition.NutritionalInformation.for_recipe(
            recipe=recipe
        )

        assert nutritional_information.protein_grams == 0
        assert nutritional_information.carbohydrates_grams == 0

    def test_for_menu_gets_correct_nutritional_information(self):
        apple = factories.Ingredient(
            name_singular="apple",
            grams_per_unit=200,
            protein_per_gram=0.1,
            carbohydrates_per_gram=0.3,
        )
        banana = factories.Ingredient(
            name_singular="banana",
            grams_per_unit=100,
            protein_per_gram=0.3,
            carbohydrates_per_gram=0.4,
        )
        apple_recipe = factories.Recipe()
        factories.RecipeIngredient(recipe=apple_recipe, ingredient=apple, quantity=4)

        banana_recipe = factories.Recipe()
        factories.RecipeIngredient(recipe=banana_recipe, ingredient=banana, quantity=3)

        no_ingredients = factories.Recipe()

        menu = factories.Menu()
        factories.MenuItem(menu=menu, recipe=apple_recipe, day=constants.Day.MONDAY)
        factories.MenuItem(menu=menu, recipe=banana_recipe, day=constants.Day.TUESDAY)
        factories.MenuItem(
            menu=menu, recipe=no_ingredients, day=constants.Day.WEDNESDAY
        )

        nutritional_information = nutrition.NutritionalInformation.for_menu(menu=menu)

        assert nutritional_information.protein_grams == 170
        assert nutritional_information.carbohydrates_grams == 360

    def test_for_menu_returns_zero_nutritional_information_when_has_no_recipes(self):
        menu = factories.Menu()

        nutritional_information = nutrition.NutritionalInformation.for_menu(menu=menu)

        assert nutritional_information.protein_grams == 0
        assert nutritional_information.carbohydrates_grams == 0

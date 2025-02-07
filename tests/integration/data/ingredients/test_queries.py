import pytest

from nutrimise.data.ingredients import queries as ingredient_queries
from nutrimise.domain import constants, ingredients
from testing.factories import data as data_factories


class TestGetIngredients:
    @pytest.mark.parametrize("matching_ingredients", [0, 1, 2])
    def test_gets_ingredients_with_passed_id_only(
        self, matching_ingredients: int, django_assert_num_queries
    ):
        ingredient_ids = [
            data_factories.Ingredient().id for _ in range(0, matching_ingredients)
        ]
        data_factories.Ingredient()  # Some other ingredient.

        expected_num_queries = min(matching_ingredients, 1)
        with django_assert_num_queries(num=expected_num_queries):
            result = ingredient_queries.get_ingredients(ingredient_ids=ingredient_ids)

        assert {ingredient.id for ingredient in result} == set(ingredient_ids)


class TestNutritionalInformationForMenuPerDay:
    def test_combines_nutritional_information_across_recipes_for_day(self):
        beef = data_factories.Ingredient(grams_per_unit=1)
        protein = data_factories.Nutrient(name="Protein")
        data_factories.IngredientNutritionalInformation(
            ingredient=beef, nutrient=protein, quantity_per_gram=0.2
        )

        beef_stew_ingredient = data_factories.RecipeIngredient(
            ingredient=beef, quantity=250
        )
        beef_lasagne_ingredient = data_factories.RecipeIngredient(
            ingredient=beef, quantity=150
        )
        beef_curry_ingredient = data_factories.RecipeIngredient(
            ingredient=beef, quantity=100
        )

        # Define a menu with two of the beef recipes both on day one.
        menu = data_factories.Menu()
        data_factories.MenuItem(
            menu=menu,
            day=1,
            meal_time=constants.MealTime.LUNCH,
            recipe=beef_stew_ingredient.recipe,
        )
        data_factories.MenuItem(
            menu=menu,
            day=1,
            meal_time=constants.MealTime.DINNER,
            recipe=beef_lasagne_ingredient.recipe,
        )
        data_factories.MenuItem(
            menu=menu,
            day=2,
            meal_time=constants.MealTime.LUNCH,
            recipe=beef_curry_ingredient.recipe,
        )

        result = ingredient_queries.get_nutritional_information_for_menu_per_day(
            menu=menu, per_serving=False
        )

        assert result == {
            1: [
                ingredients.NutritionalInformation(
                    nutrient=protein.to_domain_model(),
                    nutrient_quantity=80,  # Beef stew + beef lasagne.
                    units=constants.NutrientUnit.GRAMS,
                )
            ],
            2: [
                ingredients.NutritionalInformation(
                    nutrient=protein.to_domain_model(),
                    nutrient_quantity=20,  # Just beef curry.
                    units=constants.NutrientUnit.GRAMS,
                )
            ],
        }


class TestNutritionalInformationForRecipe:
    def test_gets_total_nutritional_information_for_recipe(self):
        beef = data_factories.Ingredient(grams_per_unit=1)
        pasta = data_factories.Ingredient(grams_per_unit=1)

        protein = data_factories.Nutrient(name="Protein")
        carbs = data_factories.Nutrient(name="Carbs")

        data_factories.IngredientNutritionalInformation(
            ingredient=beef, nutrient=protein, quantity_per_gram=0.2
        )
        data_factories.IngredientNutritionalInformation(
            ingredient=beef, nutrient=carbs, quantity_per_gram=0.1
        )
        data_factories.IngredientNutritionalInformation(
            ingredient=pasta, nutrient=protein, quantity_per_gram=0.05
        )
        data_factories.IngredientNutritionalInformation(
            ingredient=pasta, nutrient=carbs, quantity_per_gram=0.7
        )

        beef_pasta = data_factories.Recipe(name="Beef pasta", number_of_servings=3)
        data_factories.RecipeIngredient(
            recipe=beef_pasta, ingredient=beef, quantity=250
        )
        data_factories.RecipeIngredient(
            recipe=beef_pasta, ingredient=pasta, quantity=500
        )

        result = ingredient_queries.get_nutritional_information_for_recipe(
            recipe=beef_pasta, per_serving=False
        )

        assert result == [
            ingredients.NutritionalInformation(
                nutrient=ingredients.Nutrient(id=carbs.id, name=carbs.name),
                nutrient_quantity=375.0,
                units=constants.NutrientUnit.GRAMS,
            ),
            ingredients.NutritionalInformation(
                nutrient=ingredients.Nutrient(id=protein.id, name=protein.name),
                nutrient_quantity=75.0,
                units=constants.NutrientUnit.GRAMS,
            ),
        ]

    def test_gets_nutritional_information_for_recipe_per_serving(self):
        pasta = data_factories.Ingredient(grams_per_unit=1)

        protein = data_factories.Nutrient(name="Protein")
        carbs = data_factories.Nutrient(name="Carbs")

        data_factories.IngredientNutritionalInformation(
            ingredient=pasta, nutrient=protein, quantity_per_gram=0.05
        )
        data_factories.IngredientNutritionalInformation(
            ingredient=pasta, nutrient=carbs, quantity_per_gram=0.7
        )

        beef_pasta = data_factories.Recipe(name="Plain pasta", number_of_servings=2)
        data_factories.RecipeIngredient(
            recipe=beef_pasta, ingredient=pasta, quantity=500
        )

        result = ingredient_queries.get_nutritional_information_for_recipe(
            recipe=beef_pasta, per_serving=True
        )

        assert result == [
            ingredients.NutritionalInformation(
                nutrient=ingredients.Nutrient(id=carbs.id, name=carbs.name),
                nutrient_quantity=175.0,
                units=constants.NutrientUnit.GRAMS,
            ),
            ingredients.NutritionalInformation(
                nutrient=ingredients.Nutrient(id=protein.id, name=protein.name),
                nutrient_quantity=12.5,
                units=constants.NutrientUnit.GRAMS,
            ),
        ]

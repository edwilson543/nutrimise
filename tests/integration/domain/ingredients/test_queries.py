from nutrimise.data import constants
from nutrimise.domain import ingredients

from tests.factories import data as data_factories
import pytest


class TestGetIngredients:
    @pytest.mark.parametrize("matching_ingredients", [0, 1, 2])
    def test_gets_ingredients_with_passed_id_only(self, matching_ingredients: int):
        ingredient_ids = [data_factories.Ingredient().id for _ in range(0, matching_ingredients)]
        data_factories.Ingredient()  # Some other ingredient.

        result = ingredients.get_ingredients(ingredient_ids=ingredient_ids)

        assert {ingredient.id for ingredient in result} == set(ingredient_ids)


class TestNutritionalInformationForRecipe:
    def test_gets_total_ingredients_for_recipe(self):
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

        result = ingredients.get_nutritional_information_for_recipe(
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

    def test_gets_ingredients_for_recipe_per_serving(self):
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

        result = ingredients.get_nutritional_information_for_recipe(
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

# Local application imports
from domain.ingredients import nutritional_information
from tests import factories


class TestNutritionalInformationForRecipe:
    def test_gets_total_nutritional_information_for_recipe(self):
        beef = factories.Ingredient(grams_per_unit=1)
        pasta = factories.Ingredient(grams_per_unit=1)

        protein = factories.Nutrient(name="Protein")
        carbs = factories.Nutrient(name="Carbs")

        factories.IngredientNutritionalInformation(
            ingredient=beef, nutrient=protein, quantity_per_gram=0.2
        )
        factories.IngredientNutritionalInformation(
            ingredient=beef, nutrient=carbs, quantity_per_gram=0.1
        )
        factories.IngredientNutritionalInformation(
            ingredient=pasta, nutrient=protein, quantity_per_gram=0.05
        )
        factories.IngredientNutritionalInformation(
            ingredient=pasta, nutrient=carbs, quantity_per_gram=0.7
        )

        beef_pasta = factories.Recipe(name="Beef pasta", number_of_servings=3)
        factories.RecipeIngredient(recipe=beef_pasta, ingredient=beef, quantity=250)
        factories.RecipeIngredient(recipe=beef_pasta, ingredient=pasta, quantity=500)

        result = nutritional_information.get_nutritional_information_for_recipe(
            recipe=beef_pasta, per_serving=False
        )

        assert result == [
            nutritional_information.NutritionalInformation(
                nutrient_name="Carbs",
                nutrient_quantity_grams=375.0,
            ),
            nutritional_information.NutritionalInformation(
                nutrient_name="Protein",
                nutrient_quantity_grams=75.0,
            ),
        ]

    def test_gets_nutritional_information_for_recipe_per_serving(self):
        pasta = factories.Ingredient(grams_per_unit=1)

        protein = factories.Nutrient(name="Protein")
        carbs = factories.Nutrient(name="Carbs")

        factories.IngredientNutritionalInformation(
            ingredient=pasta, nutrient=protein, quantity_per_gram=0.05
        )
        factories.IngredientNutritionalInformation(
            ingredient=pasta, nutrient=carbs, quantity_per_gram=0.7
        )

        beef_pasta = factories.Recipe(name="Plain pasta", number_of_servings=2)
        factories.RecipeIngredient(recipe=beef_pasta, ingredient=pasta, quantity=500)

        result = nutritional_information.get_nutritional_information_for_recipe(
            recipe=beef_pasta, per_serving=True
        )

        assert result == [
            nutritional_information.NutritionalInformation(
                nutrient_name="Carbs",
                nutrient_quantity_grams=175.0,
            ),
            nutritional_information.NutritionalInformation(
                nutrient_name="Protein",
                nutrient_quantity_grams=12.5,
            ),
        ]

from nutrimise.domain import constants
from tests.factories import data as data_factories


class TestRecipeToDomainModel:
    def test_converts_recipe_orm_model_with_requirements_to_recipe_domain(self):
        meal_times = [constants.MealTime.LUNCH, constants.MealTime.DINNER]
        orm_recipe = data_factories.Recipe(meal_times=meal_times)

        # Make sure the recipe will have some nutritional information.
        ingredient = data_factories.Ingredient()
        data_factories.IngredientNutritionalInformation(ingredient=ingredient)
        data_factories.RecipeIngredient(recipe=orm_recipe, ingredient=ingredient)

        recipe = orm_recipe.to_domain_model()

        assert recipe.id == orm_recipe.id
        assert recipe.meal_times == tuple(meal_times)
        assert len(recipe.nutritional_information_per_serving) > 0

        assert len(recipe.ingredients) == 1
        recipe_ingredient = recipe.ingredients[0]
        assert recipe_ingredient.ingredient_id == ingredient.id

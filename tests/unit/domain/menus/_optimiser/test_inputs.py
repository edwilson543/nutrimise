import pytest

from nutrimise.domain import ingredients, recipes
from nutrimise.domain.menus._optimisation import inputs
from tests.factories import domain as domain_factories


def create_inputs(
    *,
    recipes_to_consider: tuple[recipes.Recipe, ...] = (),
    relevant_ingredients: tuple[ingredients.Ingredient, ...] = (),
):
    return inputs.OptimiserInputs(
        menu=domain_factories.Menu(),
        recipes_to_consider=recipes_to_consider,
        relevant_ingredients=relevant_ingredients,
    )


class TestOptimiserInputsLookUpRecipe:
    def test_returns_recipe_object(self):
        recipe = domain_factories.Recipe()
        inputs_ = create_inputs(recipes_to_consider=(recipe,))

        result = inputs_.look_up_recipe(recipe_id=recipe.id)

        assert result == recipe

    def test_raises_when_recipe_not_in_look_up(self):
        inputs_ = create_inputs(recipes_to_consider=())
        invalid_recipe_id = 123

        with pytest.raises(inputs.RecipeNotProvidedInLookup) as exc:
            inputs_.look_up_recipe(recipe_id=invalid_recipe_id)

        assert exc.value.recipe_id == invalid_recipe_id


class TestOptimiserInputsLookUpIngredient:
    def test_returns_ingredient_object(self):
        ingredient = domain_factories.Ingredient()
        inputs_ = create_inputs(relevant_ingredients=(ingredient,))

        result = inputs_.look_up_ingredient(ingredient_id=ingredient.id)

        assert result == ingredient

    def test_raises_when_ingredient_not_in_look_up(self):
        inputs_ = create_inputs(relevant_ingredients=())
        invalid_ingredient_id = 123

        with pytest.raises(inputs.IngredientNotProvidedInLookup) as exc:
            inputs_.look_up_ingredient(ingredient_id=invalid_ingredient_id)

        assert exc.value.ingredient_id == invalid_ingredient_id

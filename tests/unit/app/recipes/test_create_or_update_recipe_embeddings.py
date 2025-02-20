from nutrimise.app.recipes import _create_or_update_recipe_embedding
from testing.factories import domain as domain_factories


# SLightly unconventional to test a private function, but the prompt is quite important.
class TestGetPromptForRecipeEmbedding:
    def test_gets_prompt_for_recipe_with_all_fields_set(self):
        ingredient = domain_factories.Ingredient(name="Chicken")
        recipe_ingredient = domain_factories.RecipeIngredient(ingredient=ingredient)

        recipe = domain_factories.Recipe(
            name="Chicken curry",
            description="Chicken curry description",
            methodology="Chicken curry methodology",
            ingredients=(recipe_ingredient,),
        )

        prompt = _create_or_update_recipe_embedding._get_prompt_for_recipe_embedding(
            recipe=recipe
        )

        expected_prompt = """Create an embedding of this recipe that will be useful for:
- Sematic search
- Comparing it with the embeddings of meal plan requirements

Name: Chicken curry
Description: Chicken curry description
Methodology: Chicken curry methodology
Ingredients:
- Chicken"""
        assert prompt == expected_prompt

    def test_gets_prompt_for_recipe_that_only_has_name(self):
        recipe = domain_factories.Recipe(
            name="Chicken curry", description="", methodology="", ingredients=()
        )

        prompt = _create_or_update_recipe_embedding._get_prompt_for_recipe_embedding(
            recipe=recipe
        )

        expected_prompt = """Create an embedding of this recipe that will be useful for:
- Sematic search
- Comparing it with the embeddings of meal plan requirements

Name: Chicken curry"""
        assert prompt == expected_prompt

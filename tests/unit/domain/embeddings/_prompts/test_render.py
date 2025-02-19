from nutrimise.domain.embeddings._prompts import render as render_prompts
from testing.factories import domain as domain_factories


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

        prompt = render_prompts.get_prompt_for_recipe_embedding(recipe=recipe)

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

        prompt = render_prompts.get_prompt_for_recipe_embedding(recipe=recipe)

        expected_prompt = """Create an embedding of this recipe that will be useful for:
- Sematic search
- Comparing it with the embeddings of meal plan requirements

Name: Chicken curry"""
        assert prompt == expected_prompt

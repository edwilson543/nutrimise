from nutrimise.app.menus import _create_or_update_menu_embedding
from testing.factories import domain as domain_factories


# SLightly unconventional to test a private function, but the prompt is quite important.
class TestGetPromptForMenuEmbedding:
    def test_gets_prompt_for_menu_with_all_fields_set_plus_user_prompt(self):
        menu = domain_factories.Menu(
            name="My healthy meal plan",
            description="Food for next week, will re-use most weeks.",
        )

        prompt = _create_or_update_menu_embedding._get_prompt_for_menu_embedding(
            menu=menu, user_prompt="Pick the healthiest meals."
        )

        expected_prompt = """Create an embedding of this meal plan: 'My healthy meal plan'.
The meal plan's embedding will be compared with the embeddings of different recipes, to see how well they match the meal plan's requirements.
The key requirement is to please the user, who has requested: 'Pick the healthiest meals.'
The menu's description is: 'Food for next week, will re-use most weeks.'"""
        assert prompt == expected_prompt

    def test_gets_prompt_for_menu_that_only_has_name(self):
        menu = domain_factories.Menu(name="Winter bulk", description="")

        prompt = _create_or_update_menu_embedding._get_prompt_for_menu_embedding(
            menu=menu, user_prompt=None
        )

        expected_prompt = """Create an embedding of this meal plan: 'Winter bulk'.
The meal plan's embedding will be compared with the embeddings of different recipes, to see how well they match the meal plan's requirements."""
        assert prompt == expected_prompt

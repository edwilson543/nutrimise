import json
from typing import Any

import pytest
from django.test import override_settings

from nutrimise.domain import data_extraction, recipes
from nutrimise.domain.data_extraction._vendors import _openai
from testing.factories import domain as domain_factories


class TestInstantiation:
    def tests_instantiates_service_when_api_key_set(self):
        with override_settings(OPENAI_API_KEY="some-key"):
            _openai.OpenAIDataExtractionService()

    @pytest.mark.parametrize("api_key", ["", None])
    def test_raises_configuration_error_when_api_key_not_set(self, api_key: str | None):
        with (
            override_settings(OPENAI_API_KEY=api_key),
            pytest.raises(data_extraction.DataExtractionServiceMisconfigured) as exc,
        ):
            _openai.OpenAIDataExtractionService()

        assert exc.value.vendor == data_extraction.DataExtractionVendor.OPENAI


class TestExtractRecipeFromImage:
    @override_settings(OPENAI_API_KEY="some-key")
    def test_gets_output_structured_as_recipe(self, httpx_mock):
        base64_image = "My encoded image."
        ingredient = data_extraction.Ingredient.from_domain_model(
            domain_factories.Ingredient()
        )

        httpx_mock.add_response(
            url="https://api.openai.com/v1/chat/completions",
            method="POST",
            status_code=200,
            json=_extracted_recipe_response_json(ingredient=ingredient),
        )

        openai_service = _openai.OpenAIDataExtractionService()
        recipe = openai_service.extract_recipe_from_image(
            base64_image=base64_image, existing_ingredients=[ingredient]
        )

        assert recipe.name == "Some recipe"
        assert recipe.description == "Some recipe description."
        assert recipe.methodology == "Some recipe methodology."
        assert recipe.meal_times == [
            recipes.MealTime.LUNCH,
            recipes.MealTime.DINNER,
        ]
        assert recipe.number_of_servings == 7

        assert len(recipe.ingredients) == 1
        recipe_ingredient = recipe.ingredients[0]
        assert recipe_ingredient.quantity == 250.0
        assert recipe_ingredient.ingredient.name == ingredient.name
        assert recipe_ingredient.ingredient.category_name == ingredient.category_name
        assert recipe_ingredient.ingredient.units == ingredient.units
        assert recipe_ingredient.ingredient.grams_per_unit == ingredient.grams_per_unit

        assert recipe.author.first_name == "Jamie"
        assert recipe.author.last_name == "Oliver"

    @override_settings(OPENAI_API_KEY="some-key")
    def test_raises_when_open_ai_api_response_bad(self, httpx_mock):
        openai_service = _openai.OpenAIDataExtractionService()
        base64_image = "My encoded image."

        httpx_mock.add_response(
            url="https://api.openai.com/v1/chat/completions",
            method="POST",
            status_code=401,
        )

        with pytest.raises(data_extraction.UnableToExtractRecipe) as exc:
            openai_service.extract_recipe_from_image(
                base64_image=base64_image, existing_ingredients=[]
            )

        assert exc.value.vendor == openai_service.vendor
        assert exc.value.model == openai_service.model


class TestExtractRecipeFromURL:
    @override_settings(OPENAI_API_KEY="some-key")
    def test_gets_output_structured_as_recipe(self, httpx_mock):
        recipe_url = "https://recipes.com/some-recipe/"
        ingredient = data_extraction.Ingredient.from_domain_model(
            domain_factories.Ingredient()
        )

        # Mock the response to download the recipe's raw content.
        httpx_mock.add_response(
            url=recipe_url,
            method="GET",
            status_code=200,
            html="<main>Some recipe to extract</main>",
        )

        # Mock the response from OpenAI to process the recipe content.
        httpx_mock.add_response(
            url="https://api.openai.com/v1/chat/completions",
            method="POST",
            status_code=200,
            json=_extracted_recipe_response_json(ingredient=ingredient),
        )

        openai_service = _openai.OpenAIDataExtractionService()
        recipe = openai_service.extract_recipe_from_url(
            url=recipe_url, existing_ingredients=[ingredient]
        )

        assert recipe.name == "Some recipe"
        assert recipe.description == "Some recipe description."
        assert recipe.methodology == "Some recipe methodology."
        assert recipe.meal_times == [
            recipes.MealTime.LUNCH,
            recipes.MealTime.DINNER,
        ]
        assert recipe.number_of_servings == 7

        assert len(recipe.ingredients) == 1
        recipe_ingredient = recipe.ingredients[0]
        assert recipe_ingredient.quantity == 250.0
        assert recipe_ingredient.ingredient.name == ingredient.name
        assert recipe_ingredient.ingredient.category_name == ingredient.category_name
        assert recipe_ingredient.ingredient.units == ingredient.units
        assert recipe_ingredient.ingredient.grams_per_unit == ingredient.grams_per_unit

        assert recipe.author.first_name == "Jamie"
        assert recipe.author.last_name == "Oliver"

    @override_settings(OPENAI_API_KEY="some-key")
    def test_raises_when_unable_to_access_recipe_url(self, httpx_mock):
        recipe_url = "https://recipes.com/some-recipe/"
        httpx_mock.add_response(url=recipe_url, method="GET", status_code=404)
        openai_service = _openai.OpenAIDataExtractionService()

        with pytest.raises(data_extraction.UnableToExtractRecipe) as exc:
            openai_service.extract_recipe_from_url(
                url=recipe_url, existing_ingredients=[]
            )

        assert exc.value.url == recipe_url

    @override_settings(OPENAI_API_KEY="some-key")
    def test_raises_when_open_ai_api_response_bad(self, httpx_mock):
        recipe_url = "https://recipes.com/some-recipe/"
        openai_service = _openai.OpenAIDataExtractionService()

        httpx_mock.add_response(
            url=recipe_url,
            method="GET",
            status_code=200,
            html="<main>Some recipe to extract</main>",
        )

        httpx_mock.add_response(
            url="https://api.openai.com/v1/chat/completions",
            method="POST",
            status_code=401,
        )

        with pytest.raises(data_extraction.UnableToExtractRecipe) as exc:
            openai_service.extract_recipe_from_url(
                url=recipe_url, existing_ingredients=[]
            )

        assert exc.value.vendor == openai_service.vendor
        assert exc.value.model == openai_service.model


def _extracted_recipe_response_json(
    *, ingredient: data_extraction.Ingredient
) -> dict[str, Any]:
    """
    OpenAI chat completion structure response output, per the docs.
    https://platform.openai.com/docs/guides/structured-outputs
    """
    ingredient_json = {
        "id": ingredient.id,
        "name": ingredient.name,
        "category_name": ingredient.category_name,
        "units": ingredient.units,
        "grams_per_unit": ingredient.grams_per_unit,
    }
    recipe = {
        "name": "Some recipe",
        "description": "Some recipe description.",
        "methodology": "Some recipe methodology.",
        "meal_times": ["LUNCH", "DINNER"],
        "number_of_servings": 7,
        "ingredients": [{"ingredient": ingredient_json, "quantity": 250.0}],
        "author": {"first_name": "Jamie", "last_name": "Oliver"},
    }

    return {
        "id": "chatcmpl-AyCk92plBjBPBOnrcpYQ4xVC7LPZd",
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": json.dumps(recipe),
                    "role": "assistant",
                    "parsed": recipe,
                    "refusal": None,
                },
            }
        ],
    }


class TestExtractIngredientNutritionalInformation:
    @override_settings(OPENAI_API_KEY="some-key")
    def test_gets_output_structured_as_list_of_ingredient_nutritional_information(
        self, httpx_mock
    ):
        ingredient = data_extraction.Ingredient(
            id=1,
            name="Brocoli",
            category_name="Vegetable",
            units="Grams",
            grams_per_unit=1.0,
        )
        nutrient = data_extraction.Nutrient(
            id=2, name="Protein", category="MACRO", units="GRAMS"
        )

        httpx_mock.add_response(
            url="https://api.openai.com/v1/chat/completions",
            method="POST",
            status_code=200,
            json=self._response_ok_json(
                ingredient_id=ingredient.id, nutrient_id=nutrient.id
            ),
        )

        openai_service = _openai.OpenAIDataExtractionService()
        ingredient_nutritional_information = (
            openai_service.extract_ingredient_nutritional_information(
                ingredients=[ingredient], nutrients=[nutrient]
            )
        )

        assert len(ingredient_nutritional_information) == 1
        info = ingredient_nutritional_information[0]
        assert info.ingredient_id == ingredient.id
        assert info.nutrient_id == nutrient.id
        assert info.nutrient_quantity_per_gram_of_ingredient == 31.1

    @staticmethod
    def _response_ok_json(ingredient_id: int, nutrient_id: int) -> dict[str, Any]:
        """
        OpenAI chat completion structure response output, per the docs.
        https://platform.openai.com/docs/guides/structured-outputs
        """
        ingredient_nutritional_information = {
            "ingredient_id": ingredient_id,
            "nutrient_id": nutrient_id,
            "nutrient_quantity_per_gram_of_ingredient": 31.1,
        }
        parsed_data = {"data": [ingredient_nutritional_information]}

        return {
            "id": "chatcmpl-AyCk92plBjBPBOnrcpYQ4xVC7LPZd",
            "choices": [
                {
                    "finish_reason": "stop",
                    "index": 0,
                    "message": {
                        "content": json.dumps(parsed_data),
                        "refusal": None,
                        "role": "assistant",
                        "audio": None,
                        "function_call": None,
                        "tool_calls": [],
                        "parsed": parsed_data,
                    },
                }
            ],
        }

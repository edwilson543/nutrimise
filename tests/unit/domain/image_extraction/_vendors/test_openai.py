import json
from typing import Any

import pytest
from django.test import override_settings

from nutrimise.domain import constants, image_extraction
from nutrimise.domain.image_extraction._vendors import _openai


class TestInstantiation:
    def tests_instantiates_service_when_api_key_set(self):
        with override_settings(OPENAI_API_KEY="some-key"):
            _openai.OpenAIImageExtractService()

    @pytest.mark.parametrize("api_key", ["", None])
    def test_raises_configuration_error_when_api_key_not_set(self, api_key: str | None):
        with (
            override_settings(OPENAI_API_KEY=api_key),
            pytest.raises(image_extraction.ImageExtractionServiceMisconfigured) as exc,
        ):
            _openai.OpenAIImageExtractService()

        assert exc.value.vendor == image_extraction.ImageExtractionVendor.OPENAI


class TestExtractRecipeFromImage:
    @override_settings(OPENAI_API_KEY="some-key")
    def test_gets_output_structured_as_recipe(self, httpx_mock):
        openai_service = _openai.OpenAIImageExtractService()
        base64_image = "My encoded image."

        httpx_mock.add_response(
            url="https://api.openai.com/v1/chat/completions",
            method="POST",
            status_code=200,
            json=self._response_ok_json(),
        )

        recipe = openai_service.extract_recipe_from_image(base64_image=base64_image)

        assert recipe.name == "Some recipe"
        assert recipe.description == "Some recipe description."
        assert recipe.meal_times == [
            constants.MealTime.LUNCH,
            constants.MealTime.DINNER,
        ]
        assert recipe.number_of_servings == 7

        assert len(recipe.ingredients) == 1
        recipe_ingredient = recipe.ingredients[0]
        assert recipe_ingredient.quantity == 250.0
        assert recipe_ingredient.ingredient.name == "Beef"
        assert recipe_ingredient.ingredient.category_name == "Meat"
        assert recipe_ingredient.ingredient.units == "Grams"
        assert recipe_ingredient.ingredient.grams_per_unit == 1.0

    @override_settings(OPENAI_API_KEY="some-key")
    def test_raises_when_open_ai_api_response_bad(self, httpx_mock):
        openai_service = _openai.OpenAIImageExtractService()
        base64_image = "My encoded image."

        httpx_mock.add_response(
            url="https://api.openai.com/v1/chat/completions",
            method="POST",
            status_code=401,
        )

        with pytest.raises(image_extraction.UnableToExtractRecipeFromImage) as exc:
            openai_service.extract_recipe_from_image(base64_image=base64_image)

        assert exc.value.vendor == openai_service.vendor
        assert exc.value.model == openai_service.model

    def _response_ok_json(self) -> dict[str, Any]:
        """
        OpenAI chat completion structure response output, per the docs.
        https://platform.openai.com/docs/guides/structured-outputs
        """
        ingredient = {
            "name": "Beef",
            "category_name": "Meat",
            "units": "Grams",
            "grams_per_unit": 1.0,
        }
        recipe = {
            "name": "Some recipe",
            "description": "Some recipe description.",
            "meal_times": ["LUNCH", "DINNER"],
            "number_of_servings": 7,
            "ingredients": [{"ingredient": ingredient, "quantity": 250.0}],
        }

        return {
            "id": "chatcmpl-AyCk92plBjBPBOnrcpYQ4xVC7LPZd",
            "choices": [
                {
                    "finish_reason": "stop",
                    "index": 0,
                    "logprobs": None,
                    "message": {
                        "content": json.dumps(recipe),
                        "refusal": None,
                        "role": "assistant",
                        "audio": None,
                        "function_call": None,
                        "tool_calls": [],
                        "parsed": recipe,
                    },
                }
            ],
            "created": 1738912029,
            "model": "gpt-4o-2024-08-06",
            "object": "chat.completion",
            "service_tier": "default",
            "system_fingerprint": "fp_4691090a87",
        }

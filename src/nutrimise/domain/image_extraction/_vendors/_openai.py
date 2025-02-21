import attrs
import openai
from django.conf import settings
from openai.types import chat as openai_chat_types

from nutrimise.domain.image_extraction import _constants, _output_structure

from . import _base


def _get_client() -> openai.Client:
    if not (api_key := settings.OPENAI_API_KEY):
        raise _base.ImageExtractionServiceMisconfigured(
            vendor=_constants.ImageExtractionVendor.OPENAI
        )
    return openai.Client(api_key=api_key)


@attrs.frozen
class OpenAIImageExtractionService(_base.ImageExtractionService):
    model: _constants.ImageExtractionModel = _constants.ImageExtractionModel.GPT_4O
    vendor: _constants.ImageExtractionVendor = _constants.ImageExtractionVendor.OPENAI
    _client: openai.Client = attrs.field(factory=_get_client, init=False)

    def extract_recipe_from_image(
        self,
        *,
        base64_image: str,
        existing_ingredients: list[_output_structure.Ingredient],
    ) -> _output_structure.Recipe:
        messages = _get_image_extraction_prompt(
            base64_image=base64_image, existing_ingredients=existing_ingredients
        )

        try:
            response = self._client.beta.chat.completions.parse(
                model=self.model.value,
                messages=messages,
                response_format=_output_structure.Recipe,
            )
        except openai.APIError as exc:
            raise _base.UnableToExtractRecipeFromImage(
                vendor=self.vendor, model=self.model
            ) from exc

        if not (recipe := response.choices[0].message.parsed):
            raise _base.UnableToExtractRecipeFromImage(
                vendor=self.vendor, model=self.model
            )

        return recipe


def _get_image_extraction_prompt(
    *,
    base64_image: str,
    existing_ingredients: list[_output_structure.Ingredient],
) -> list[openai_chat_types.ChatCompletionMessageParam]:
    def _get_system_prompt() -> openai_chat_types.ChatCompletionSystemMessageParam:
        return {
            "role": "system",
            "content": "Extract the information from the given image in the specified format.",
        }

    def _get_ingredients_system_prompt(
        *, existing_ingredients: list[_output_structure.Ingredient]
    ) -> openai_chat_types.ChatCompletionSystemMessageParam:
        ingredients_json = [
            ingredient.model_dump_json() for ingredient in existing_ingredients
        ]

        prompt = f"""Consider the following list of ingredients:
        {ingredients_json}
        For each ingredient you extract from the recipe image:
        - If the ingredient is already in the list, ensure your response exactly matches the details provided (including name, category, units, and grams per unit).
        - If the ingredient is not in the list, you may include it as a new ingredient in your response while maintaining consistency in format."
        """

        return {"role": "system", "content": prompt}

    def _get_user_prompt(
        *, base64_image: str
    ) -> openai_chat_types.ChatCompletionUserMessageParam:
        return {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }

    return [
        _get_system_prompt(),
        _get_ingredients_system_prompt(existing_ingredients=existing_ingredients),
        _get_user_prompt(base64_image=base64_image),
    ]

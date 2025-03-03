import attrs
import bs4
import httpx
import openai
from django.conf import settings
from openai.types import chat as openai_chat_types

from nutrimise.domain.data_extraction import _constants, _output_structure

from . import _base


def _get_client() -> openai.Client:
    if not (api_key := settings.OPENAI_API_KEY):
        raise _base.DataExtractionServiceMisconfigured(
            vendor=_constants.DataExtractionVendor.OPENAI
        )
    return openai.Client(api_key=api_key)


@attrs.frozen
class OpenAIDataExtractionService(_base.DataExtractionService):
    model: _constants.DataExtractionModel = _constants.DataExtractionModel.GPT_4O
    vendor: _constants.DataExtractionVendor = _constants.DataExtractionVendor.OPENAI
    _client: openai.Client = attrs.field(factory=_get_client, init=False)

    def extract_recipe_from_image(
        self,
        *,
        base64_image: str,
        existing_ingredients: list[_output_structure.Ingredient],
    ) -> _output_structure.Recipe:
        messages = _get_data_extraction_prompt(
            base64_image=base64_image, existing_ingredients=existing_ingredients
        )

        try:
            response = self._client.beta.chat.completions.parse(
                model=self.model.value,
                messages=messages,
                response_format=_output_structure.Recipe,
            )
        except openai.APIError as exc:
            raise _base.UnableToExtractRecipe(
                vendor=self.vendor, model=self.model
            ) from exc

        if not (recipe := response.choices[0].message.parsed):
            raise _base.UnableToExtractRecipe(
                vendor=self.vendor, model=self.model
            )

        return recipe

    def extract_ingredient_nutritional_information(
        self,
        *,
        ingredients: list[_output_structure.Ingredient],
        nutrients: list[_output_structure.Nutrient],
    ) -> list[_output_structure.IngredientNutritionalInformation]:
        messages = _get_nutritional_info_extraction_prompt(
            ingredients=ingredients, nutrients=nutrients
        )

        try:
            response = self._client.beta.chat.completions.parse(
                model=self.model.value,
                messages=messages,
                response_format=_output_structure.IngredientNutritionalInformationList,
            )
        except openai.APIError as exc:
            raise _base.UnableToExtractIngredientNutritionalInformation(
                vendor=self.vendor, model=self.model
            ) from exc

        if not (info_list := response.choices[0].message.parsed):
            raise _base.UnableToExtractIngredientNutritionalInformation(
                vendor=self.vendor, model=self.model
            )

        return info_list.data


def _get_data_extraction_prompt(
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


def _get_nutritional_info_extraction_prompt(
    *,
    ingredients: list[_output_structure.Ingredient],
    nutrients: list[_output_structure.Nutrient],
) -> list[openai_chat_types.ChatCompletionMessageParam]:
    ingredients_json = [ingredient.model_dump_json() for ingredient in ingredients]
    nutrients_json = [nutrient.model_dump_json() for nutrient in nutrients]

    prompt = f"""You are given the follow data:
    - A list of ingredients, in JSON format: {ingredients_json}
    - A list of nutrients, in JSON format: {nutrients_json}
    
    Task:
    For every ingredient:
    - Determine the quantity of every nutrient in one gram of that ingredient.  
    - Ensure that the quantity of the nutrient is specified in terms of the nutrient units provided.  
    - If a nutrient is not present in an ingredient or if no data is available, return a quantity of `0`.
    """

    return [
        {
            "role": "system",
            "content": "Extract the ingredient nutritional information in the specified format.",
        },
        {"role": "user", "content": prompt},
    ]

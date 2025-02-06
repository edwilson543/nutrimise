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
class OpenAIImageExtractService(_base.ImageExtractionService):
    model: _constants.ImageExtractionModel = _constants.ImageExtractionModel.GPT_4O
    vendor: _constants.ImageExtractionVendor = _constants.ImageExtractionVendor.OPENAI
    _client: openai.Client = attrs.field(factory=_get_client, init=False)

    def extract_recipe_from_image(
        self, *, base64_image: str
    ) -> _output_structure.Recipe:
        system_prompt: openai_chat_types.ChatCompletionSystemMessageParam = {
            "role": "system",
            "content": "Extract the information from the given image in the specified format.",
        }
        user_prompt: openai_chat_types.ChatCompletionUserMessageParam = {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }

        try:
            response = self._client.beta.chat.completions.parse(
                model=self.model.value,
                messages=[system_prompt, user_prompt],
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

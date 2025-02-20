import attrs
import numpy as np
import openai
from django.conf import settings

from nutrimise.domain.embeddings import _embedding

from . import _base


def _get_client() -> openai.Client:
    if not (api_key := settings.OPENAI_API_KEY):
        raise _base.EmbeddingServiceMisconfigured(
            vendor=_embedding.EmbeddingVendor.OPENAI
        )
    return openai.Client(api_key=api_key)


@attrs.frozen
class OpenAIEmbeddingService(_base.EmbeddingService):
    model: _embedding.EmbeddingModel = _embedding.EmbeddingModel.TEXT_EMBEDDING_3_LARGE
    vendor: _embedding.EmbeddingVendor = _embedding.EmbeddingVendor.OPENAI
    _client: openai.Client = attrs.field(factory=_get_client, init=False)

    def get_embedding(self, *, text: str) -> _embedding.Embedding:
        try:
            response = self._client.embeddings.create(
                model=self.model.value,
                input=text,
                dimensions=_embedding.EMBEDDING_DIMENSIONS,
            )
        except openai.APIError as exc:
            raise _base.UnableToGetEmbedding(
                vendor=self.vendor, model=self.model
            ) from exc

        vector = response.data[0].embedding
        return self._init_embedding(text=text, vector=np.asarray(vector))

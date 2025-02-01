import attrs
import numpy as np

from nutrimise.domain.embeddings import _embedding

from . import _base


@attrs.frozen
class FakeEmbeddingService(_base.EmbeddingService):
    model: _embedding.EmbeddingModel = _embedding.EmbeddingModel.FAKE
    vendor: _embedding.EmbeddingVendor = _embedding.EmbeddingVendor.FAKE

    _created_embeddings: list[_embedding.Embedding] = attrs.field(
        factory=list, init=False
    )

    def get_embedding(self, *, text: str) -> _embedding.Embedding:
        embedding = _embedding.Embedding(
            vector=self.stub_vector,
            embedded_content_hash=self._get_hash_for_text(text=text),
            vendor=self.vendor,
            model=self.model,
        )
        self._created_embeddings.append(embedding)
        return embedding

    @property
    def created_embeddings(self) -> list[_embedding.Embedding]:
        return self._created_embeddings

    @property
    def stub_vector(self) -> np.ndarray:
        return np.ones(_embedding.EMBEDDING_DIMENSIONS)

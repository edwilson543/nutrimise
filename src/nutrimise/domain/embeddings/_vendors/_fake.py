import attrs
import numpy as np

from nutrimise.domain.embeddings import _embedding

from . import _base


@attrs.frozen
class FakeEmbeddingService(_base.EmbeddingService):
    model: _embedding.EmbeddingModel = _embedding.EmbeddingModel.FAKE
    vendor: _embedding.EmbeddingVendor = _embedding.EmbeddingVendor.FAKE

    @property
    def stub_vector(self) -> np.ndarray:
        return np.ones(_embedding.EMBEDDING_DIMENSIONS)

    def get_embedding(self, *, text: str) -> _embedding.Embedding:
        return _embedding.Embedding(
            vector=self.stub_vector,
            vendor=self.vendor,
            model=self.model,
        )

from nutrimise.domain.embeddings import _embedding

from . import _base


class FakeEmbeddingService(_base.EmbeddingService):
    vendor = _embedding.EmbeddingVendor.FAKE

    @property
    def stub_vector(self) -> list[float]:
        return [1.0] + [0] * (_embedding.EMBEDDING_DIMENSIONS - 1)

    def get_embedding(
        self, *, text: str, model: _embedding.EmbeddingModel
    ) -> _embedding.Embedding:
        return _embedding.Embedding(
            vector=self.stub_vector,
            vendor=self.vendor,
            model=_embedding.EmbeddingModel.FAKE,
        )

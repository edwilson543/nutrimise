import attrs

from nutrimise.domain.embeddings import _embedding

from . import _base


@attrs.frozen
class BrokenEmbeddingService(_base.EmbeddingService):
    model: _embedding.EmbeddingModel = _embedding.EmbeddingModel.FAKE
    vendor: _embedding.EmbeddingVendor = _embedding.EmbeddingVendor.BROKEN

    def get_embedding(self, *, text: str) -> _embedding.Embedding:
        raise _base.UnableToGetEmbedding(vendor=self.vendor, model=self.model)

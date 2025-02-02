import attrs

from nutrimise.domain.embeddings import _embedding

from . import _base


@attrs.frozen
class BrokenEmbeddingService(_base.EmbeddingService):
    model: _embedding.EmbeddingModel = _embedding.EmbeddingModel.FAKE
    vendor: _embedding.EmbeddingVendor = _embedding.EmbeddingVendor.BROKEN

    _created_embeddings: list[_embedding.Embedding] = attrs.field(
        factory=list, init=False
    )

    def get_embedding(self, *, text: str) -> _embedding.Embedding:
        raise _base.UnableToGetEmbedding(vendor=self.vendor, model=self.model)

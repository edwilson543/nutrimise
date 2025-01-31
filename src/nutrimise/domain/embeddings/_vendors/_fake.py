from nutrimise.data import constants

from . import _base


class FakeEmbeddingService(_base.EmbeddingService):
    vendor = constants.EmbeddingVendor.FAKE

    @property
    def stub_embedding(self) -> list[float]:
        return [1.0] + [0] * (constants.EMBEDDING_DIMENSIONS - 1)

    def get_embedding(
        self, *, text: str, model: constants.EmbeddingModel
    ) -> list[float]:
        return self.stub_embedding

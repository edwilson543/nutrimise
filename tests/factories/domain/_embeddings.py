import factory
import numpy as np

from nutrimise.domain import embeddings


class Embedding(factory.Factory):
    vector = factory.LazyFunction(lambda: Embedding.stub_vector())
    embedded_content_hash = factory.Sequence(lambda n: f"embedded-content-hash-{n}")
    vendor = embeddings.EmbeddingVendor.FAKE
    model = embeddings.EmbeddingModel.FAKE

    class Meta:
        model = embeddings.Embedding

    @staticmethod
    def stub_vector() -> np.ndarray:
        return np.ones(embeddings.EMBEDDING_DIMENSIONS)

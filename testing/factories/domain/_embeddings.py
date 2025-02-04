import factory
import numpy as np

from nutrimise.domain import embeddings


class Embedding(factory.Factory):
    vector = factory.Transformer(
        factory.LazyFunction(embeddings.get_stub_vector_embedding), transform=np.asarray
    )
    prompt_hash = factory.Sequence(lambda n: f"embedded-content-hash-{n}")
    vendor = embeddings.EmbeddingVendor.FAKE
    model = embeddings.EmbeddingModel.FAKE

    class Meta:
        model = embeddings.Embedding

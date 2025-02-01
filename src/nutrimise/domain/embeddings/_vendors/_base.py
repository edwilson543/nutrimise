import abc

import attrs

from nutrimise.domain.embeddings import _embedding


@attrs.frozen
class UnableToGetEmbedding(Exception):
    vendor: _embedding.EmbeddingVendor
    model: _embedding.EmbeddingModel


@attrs.frozen
class EmbeddingService(abc.ABC):
    model: _embedding.EmbeddingModel
    vendor: _embedding.EmbeddingVendor

    @abc.abstractmethod
    def get_embedding(self, *, text: str) -> _embedding.Embedding:
        """
        Get an embedding for the passed text.

        :raises UnableToGetEmbedding: If the service is unable to produce an embedding
            for some reason.
        """
        raise NotImplementedError

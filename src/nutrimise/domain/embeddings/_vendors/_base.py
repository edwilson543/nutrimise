import abc

import attrs

from nutrimise.domain.embeddings import _embedding


@attrs.frozen
class UnableToGetEmbedding(Exception):
    vendor: _embedding.EmbeddingVendor
    model: _embedding.EmbeddingModel


class EmbeddingService(abc.ABC):
    vendor: _embedding.EmbeddingVendor

    @abc.abstractmethod
    def get_embedding(
        self, *, text: str, model: _embedding.EmbeddingModel
    ) -> _embedding.Embedding:
        """
        Get an embedding for the passed text.

        :raises UnableToGetEmbedding: If the service is unable to produce an embedding
            for some reason.
        """
        raise NotImplementedError

import abc

import attrs
import numpy as np

from nutrimise.domain.embeddings import _embedding, _helpers


@attrs.frozen
class EmbeddingServiceMisconfigured(Exception):
    vendor: _embedding.EmbeddingVendor


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

    def _init_embedding(self, *, text: str, vector: np.ndarray) -> _embedding.Embedding:
        prompt_hash = _helpers.get_hash_for_text(text=text)
        return _embedding.Embedding(
            vector=vector,
            prompt_hash=prompt_hash,
            vendor=self.vendor,
            model=self.model,
        )

    @staticmethod
    def _get_hash_for_text(text: str) -> str:
        return _helpers.get_hash_for_text(text=text)

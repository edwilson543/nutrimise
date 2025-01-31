import abc

import attrs

from nutrimise.data import constants


@attrs.frozen
class UnableToGetEmbedding(Exception):
    vendor: constants.EmbeddingVendor
    model: constants.EmbeddingModel


class EmbeddingService(abc.ABC):
    vendor: constants.EmbeddingVendor

    @abc.abstractmethod
    def get_embedding(
        self, *, text: str, model: constants.EmbeddingModel
    ) -> list[float]:
        """
        Get an embedding for the passed text.

        :raises UnableToGetEmbedding: If the service is unable to produce an embedding
            for some reason.
        """
        raise NotImplementedError

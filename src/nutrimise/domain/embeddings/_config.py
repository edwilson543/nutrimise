import attrs
from django.conf import settings

from . import _embedding, _vendors


@attrs.frozen
class EmbeddingServiceMisconfigured(Exception):
    vendor: _embedding.EmbeddingVendor


def get_embedding(*, text: str) -> _embedding.Embedding:
    """
    Get an embedding, using the installed embedding service.

    :raises EmbeddingServiceNotConfigured: If the there embedding service is not
        configured correctly.
    :raises UnableToGetEmbedding: If the installed embedding service is unable
        to produce an embedding.
    """
    vendor = _embedding.EmbeddingVendor(settings.EMBEDDING_VENDOR)
    service = _get_embedding_service_for_vendor(vendor)
    model = _get_model_for_vendor(vendor)

    return service.get_embedding(text=text, model=model)


def _get_embedding_service_for_vendor(
    vendor: _embedding.EmbeddingVendor,
) -> _vendors.EmbeddingService:
    match vendor:
        case vendor.FAKE | vendor.FAKE_NO_MODEL:
            return _vendors.FakeEmbeddingService()
        case _:
            raise EmbeddingServiceMisconfigured(vendor=vendor)


def _get_model_for_vendor(
    vendor: _embedding.EmbeddingVendor,
) -> _embedding.EmbeddingModel:
    mapping = {
        _embedding.EmbeddingVendor.OPEN_AI: _embedding.EmbeddingModel.TEXT_EMBEDDING_3_SMALL,
        _embedding.EmbeddingVendor.FAKE: _embedding.EmbeddingModel.FAKE,
    }

    try:
        return mapping[vendor]
    except KeyError as exc:
        raise EmbeddingServiceMisconfigured(vendor=vendor) from exc

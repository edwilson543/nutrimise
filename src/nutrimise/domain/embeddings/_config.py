import attrs
from django.conf import settings

from . import _embedding, _vendors


@attrs.frozen
class EmbeddingServiceMisconfigured(Exception):
    vendor: _embedding.EmbeddingVendor


def get_embedding_service() -> _vendors.EmbeddingService:
    """
    Get the installed embedding service.

    :raises EmbeddingServiceNotConfigured: If the there embedding service is not
        configured correctly.
    """
    vendor = _embedding.EmbeddingVendor(settings.EMBEDDING_VENDOR)
    return _get_embedding_service_for_vendor(vendor)


def _get_embedding_service_for_vendor(
    vendor: _embedding.EmbeddingVendor,
) -> _vendors.EmbeddingService:
    model = _get_model_for_vendor(vendor)

    match vendor:
        case vendor.FAKE | vendor.FAKE_NO_MODEL:
            return _vendors.FakeEmbeddingService(vendor=vendor, model=model)
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

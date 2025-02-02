from django.conf import settings

from . import _embedding, _vendors


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
    match vendor:
        case vendor.FAKE:
            return _vendors.FakeEmbeddingService()
        case vendor.BROKEN:
            return _vendors.BrokenEmbeddingService()
        case _:
            raise _vendors.EmbeddingServiceMisconfigured(vendor=vendor)

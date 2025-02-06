from django.conf import settings

from . import _constants, _vendors


def get_image_extraction_service() -> _vendors.ImageExtractionService:
    vendor = _constants.ImageExtractionVendor(settings.IMAGE_EXTRACTION_VENDOR)
    return _get_image_extraction_service_for_vendor(vendor=vendor)


def _get_image_extraction_service_for_vendor(
    vendor: _constants.ImageExtractionVendor,
) -> _vendors.ImageExtractionService:
    match vendor:
        case vendor.OPENAI:
            return _vendors.OpenAIImageExtractService()
        case vendor.FAKE:
            return _vendors.FakeImageExtractService()
        case _:
            raise _vendors.ImageExtractionServiceMisconfigured(vendor=vendor)

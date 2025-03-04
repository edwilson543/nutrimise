from django.conf import settings

from . import _constants, _vendors


def get_data_extraction_service() -> _vendors.DataExtractionService:
    vendor = _constants.DataExtractionVendor(settings.DATA_EXTRACTION_VENDOR)
    return _get_data_extraction_service_for_vendor(vendor=vendor)


def _get_data_extraction_service_for_vendor(
    vendor: _constants.DataExtractionVendor,
) -> _vendors.DataExtractionService:
    match vendor:
        case vendor.OPENAI:
            return _vendors.OpenAIDataExtractionService()
        case vendor.FAKE:
            return _vendors.FakeDataExtractionService()
        case vendor.BROKEN:
            return _vendors.BrokenDataExtractionService()
        case _:
            raise _vendors.DataExtractionServiceMisconfigured(vendor=vendor)

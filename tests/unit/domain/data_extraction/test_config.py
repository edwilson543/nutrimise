import pytest
from django.test import override_settings

from nutrimise.domain import data_extraction
from nutrimise.domain.data_extraction import _vendors


class TestGetDataExtractionService:
    @override_settings(DATA_EXTRACTION_VENDOR="OPENAI")
    def test_gets_openai_service_when_openai_vendor_installed(self):
        service = data_extraction.get_data_extraction_service()

        assert isinstance(service, _vendors.OpenAIDataExtractionService)

    @override_settings(DATA_EXTRACTION_VENDOR="FAKE")
    def test_gets_fake_service_when_fake_vendor_installed(self):
        service = data_extraction.get_data_extraction_service()

        assert isinstance(service, _vendors.FakeDataExtractionService)

    @override_settings(DATA_EXTRACTION_VENDOR="BROKEN")
    def test_gets_broken_service_when_broken_vendor_installed(self):
        service = data_extraction.get_data_extraction_service()

        assert isinstance(service, _vendors.BrokenDataExtractionService)

    @override_settings(DATA_EXTRACTION_VENDOR="FAKE_NO_SERVICE")
    def test_raises_when_no_service_is_installed_for_vendor(self):
        with pytest.raises(data_extraction.DataExtractionServiceMisconfigured) as exc:
            data_extraction.get_data_extraction_service()

        assert exc.value.vendor == data_extraction.DataExtractionVendor.FAKE_NO_SERVICE

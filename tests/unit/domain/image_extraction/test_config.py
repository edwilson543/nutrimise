import pytest
from django.test import override_settings

from nutrimise.domain import image_extraction
from nutrimise.domain.image_extraction import _vendors


class TestGetImageExtractionService:
    @override_settings(IMAGE_EXTRACTION_VENDOR="OPENAI")
    def test_gets_openai_service_when_openai_vendor_installed(self):
        service = image_extraction.get_image_extraction_service()

        assert isinstance(service, _vendors.OpenAIImageExtractionService)

    @override_settings(IMAGE_EXTRACTION_VENDOR="FAKE")
    def test_gets_fake_service_when_fake_vendor_installed(self):
        service = image_extraction.get_image_extraction_service()

        assert isinstance(service, _vendors.FakeImageExtractionService)

    @override_settings(IMAGE_EXTRACTION_VENDOR="BROKEN")
    def test_gets_broken_service_when_broken_vendor_installed(self):
        service = image_extraction.get_image_extraction_service()

        assert isinstance(service, _vendors.BrokenImageExtractionService)

    @override_settings(IMAGE_EXTRACTION_VENDOR="FAKE_NO_SERVICE")
    def test_raises_when_no_service_is_installed_for_vendor(self):
        with pytest.raises(image_extraction.ImageExtractionServiceMisconfigured) as exc:
            image_extraction.get_image_extraction_service()

        assert (
            exc.value.vendor == image_extraction.ImageExtractionVendor.FAKE_NO_SERVICE
        )

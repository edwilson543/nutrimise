import pytest
from django.test import override_settings

from nutrimise.domain import image_extraction


class TestGetImageExtractionService:
    @override_settings(IMAGE_EXTRACTION_VENDOR="OPENAI")
    def test_gets_openai_embedding_service_when_openai_embedding_service_installed(
        self,
    ):
        service = image_extraction.get_image_extraction_service()

        assert isinstance(service, image_extraction.OpenAIImageExtractService)

    @override_settings(IMAGE_EXTRACTION_VENDOR="FAKE")
    def test_gets_fake_embedding_when_fake_embedding_service_installed(self):
        service = image_extraction.get_image_extraction_service()

        assert isinstance(service, image_extraction.FakeImageExtractService)

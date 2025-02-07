import pytest
from django.test import override_settings

from nutrimise.domain import embeddings


class TestGetEmbeddingService:
    @override_settings(EMBEDDING_VENDOR="OPENAI")
    def test_gets_openai_embedding_service_when_openai_embedding_service_installed(
        self,
    ):
        service = embeddings.get_embedding_service()

        assert isinstance(service, embeddings.OpenAIEmbeddingService)
        assert service.vendor == embeddings.EmbeddingVendor.OPENAI
        assert service.model == embeddings.EmbeddingModel.TEXT_EMBEDDING_3_SMALL

    @override_settings(EMBEDDING_VENDOR="FAKE")
    def test_gets_fake_embedding_when_fake_embedding_service_installed(self):
        service = embeddings.get_embedding_service()

        assert isinstance(service, embeddings.FakeEmbeddingService)
        assert service.vendor == embeddings.EmbeddingVendor.FAKE
        assert service.model == embeddings.EmbeddingModel.FAKE

    @override_settings(EMBEDDING_VENDOR="BROKEN")
    def test_gets_broken_embedding_when_broken_embedding_service_installed(self):
        service = embeddings.get_embedding_service()

        assert isinstance(service, embeddings.BrokenEmbeddingService)
        assert service.vendor == embeddings.EmbeddingVendor.BROKEN
        assert service.model == embeddings.EmbeddingModel.FAKE

    @override_settings(EMBEDDING_VENDOR="FAKE_NO_SERVICE")
    def test_raises_when_no_service_is_installed_for_vendor(self):
        with pytest.raises(embeddings.EmbeddingServiceMisconfigured) as exc:
            embeddings.get_embedding_service()

        assert exc.value.vendor == embeddings.EmbeddingVendor.FAKE_NO_SERVICE

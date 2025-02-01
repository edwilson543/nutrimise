import pytest
from django.test import override_settings

from nutrimise.domain import embeddings


class TestGetEmbedding:
    @override_settings(EMBEDDING_VENDOR="FAKE")
    def test_gets_fake_embedding_when_fake_embedding_service_installed(self):
        service = embeddings.get_embedding_service()

        assert service.vendor == embeddings.EmbeddingVendor.FAKE
        assert service.model == embeddings.EmbeddingModel.FAKE

    @override_settings(EMBEDDING_VENDOR="FAKE_NO_MODEL")
    def test_raises_when_no_service_is_installed_for_vendor(self):
        with pytest.raises(embeddings.EmbeddingServiceMisconfigured) as exc:
            embeddings.get_embedding_service()

        assert exc.value.vendor == embeddings.EmbeddingVendor.FAKE_NO_MODEL

    @override_settings(EMBEDDING_VENDOR="FAKE_NO_SERVICE")
    def test_raises_when_no_model_is_installed_for_vendor(self):
        with pytest.raises(embeddings.EmbeddingServiceMisconfigured) as exc:
            embeddings.get_embedding_service()

        assert exc.value.vendor == embeddings.EmbeddingVendor.FAKE_NO_SERVICE

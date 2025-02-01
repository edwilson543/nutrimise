import pytest
from django.test import override_settings

from nutrimise.domain import embeddings
from nutrimise.domain.embeddings import _vendors as embeddings_vendors


class TestGetEmbedding:
    @override_settings(EMBEDDING_VENDOR="FAKE")
    def test_gets_fake_embedding_when_fake_embedding_service_installed(self):
        text = "some text"

        embedding = embeddings.get_embedding(text=text)

        expected_vector = embeddings_vendors.FakeEmbeddingService().stub_embedding
        assert embedding.vendor == embeddings.EmbeddingVendor.FAKE
        assert embedding.model == embeddings.EmbeddingModel.FAKE
        assert embedding.embedding == expected_vector

    @override_settings(EMBEDDING_VENDOR="FAKE_NO_MODEL")
    def test_raises_when_no_service_is_installed_for_vendor(self):
        text = "some text"

        with pytest.raises(embeddings.EmbeddingServiceMisconfigured) as exc:
            embeddings.get_embedding(text=text)

        assert exc.value.vendor == embeddings.EmbeddingVendor.FAKE_NO_MODEL

    @override_settings(EMBEDDING_VENDOR="FAKE_NO_SERVICE")
    def test_raises_when_no_model_is_installed_for_vendor(self):
        text = "some text"

        with pytest.raises(embeddings.EmbeddingServiceMisconfigured) as exc:
            embeddings.get_embedding(text=text)

        assert exc.value.vendor == embeddings.EmbeddingVendor.FAKE_NO_SERVICE

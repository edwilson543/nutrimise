import pytest

from django.test import override_settings

from nutrimise.domain import constants
from nutrimise.domain.embeddings import _vendors as embeddings_vendors
from nutrimise.domain.embeddings import config as embeddings_config


class TestGetEmbedding:
    @override_settings(EMBEDDING_VENDOR="FAKE")
    def test_gets_fake_embedding_when_fake_embedding_service_installed(self):
        text = "some text"

        embedding = embeddings_config.get_embedding(text=text)

        expected_embedding = embeddings_vendors.FakeEmbeddingService().stub_embedding
        assert embedding == expected_embedding

    @override_settings(EMBEDDING_VENDOR="FAKE_NO_MODEL")
    def test_raises_when_no_service_is_installed_for_vendor(self):
        text = "some text"

        with pytest.raises(embeddings_config.EmbeddingServiceMisconfigured) as exc:
            embeddings_config.get_embedding(text=text)

        assert exc.value.vendor == constants.EmbeddingVendor.FAKE_NO_MODEL

    @override_settings(EMBEDDING_VENDOR="FAKE_NO_SERVICE")
    def test_raises_when_no_model_is_installed_for_vendor(self):
        text = "some text"

        with pytest.raises(embeddings_config.EmbeddingServiceMisconfigured) as exc:
            embeddings_config.get_embedding(text=text)

        assert exc.value.vendor == constants.EmbeddingVendor.FAKE_NO_SERVICE

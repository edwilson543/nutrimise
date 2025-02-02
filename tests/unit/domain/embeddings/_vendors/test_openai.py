from typing import Any

import numpy as np
import pytest
from django.test import override_settings
from numpy import testing as np_testing

from nutrimise.domain import embeddings
from nutrimise.domain.embeddings._vendors import _openai


class TestInstantiation:
    def tests_instantiates_service_when_api_key_set(self):
        with override_settings(OPENAI_API_KEY="some-key"):
            _openai.OpenAIEmbeddingService()

    @pytest.mark.parametrize("api_key", ["", None])
    def test_raises_configuration_error_when_api_key_not_set(self, api_key: str | None):
        with (
            override_settings(OPENAI_API_KEY=api_key),
            pytest.raises(embeddings.EmbeddingServiceMisconfigured) as exc,
        ):
            _openai.OpenAIEmbeddingService()

        assert exc.value.vendor == embeddings.EmbeddingVendor.OPENAI


class TestGetEmbedding:
    @override_settings(OPENAI_API_KEY="some-key")
    def test_gets_embedding_when_open_ai_api_response_ok(self, httpx_mock):
        openai_service = _openai.OpenAIEmbeddingService()
        text = "Some text to embed."

        httpx_mock.add_response(
            url="https://api.openai.com/v1/embeddings",
            method="POST",
            status_code=200,
            json=self._response_ok_json(),
        )

        embedding = openai_service.get_embedding(text=text)

        np_testing.assert_array_equal(embedding.vector, self._stub_embedding)
        assert embedding.embedded_content_hash == "7102d8d4aeaad1fa2b931d49d32a62dc"
        assert embedding.vendor == embeddings.EmbeddingVendor.OPENAI
        assert embedding.model == embeddings.EmbeddingModel.TEXT_EMBEDDING_3_SMALL

    @override_settings(OPENAI_API_KEY="some-key")
    def test_raises_when_open_ai_api_response_bad(self, httpx_mock):
        openai_service = _openai.OpenAIEmbeddingService()
        text = "Some text to embed."

        httpx_mock.add_response(
            url="https://api.openai.com/v1/embeddings",
            method="POST",
            status_code=401,
        )

        with pytest.raises(embeddings.UnableToGetEmbedding) as exc:
            openai_service.get_embedding(text=text)

        assert exc.value.vendor == embeddings.EmbeddingVendor.OPENAI
        assert exc.value.model == embeddings.EmbeddingModel.TEXT_EMBEDDING_3_SMALL

    def _response_ok_json(self) -> dict[str, Any]:
        """
        OpenAI embeddings response object, per the docs.
        https://platform.openai.com/docs/api-reference/embeddings/create
        """
        return {
            "object": "list",
            "data": [
                {
                    "object": "embedding",
                    "index": 0,
                    "embedding": list(self._stub_embedding),
                }
            ],
            "model": "text-embedding-3-small",
            "usage": {"prompt_tokens": 5, "total_tokens": 5},
        }

    @property
    def _stub_embedding(self) -> np.ndarray:
        return np.ones(embeddings.EMBEDDING_DIMENSIONS)

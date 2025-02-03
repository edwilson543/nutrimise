from numpy import testing as np_testing

from nutrimise.domain import embeddings


class TestGetEmbedding:
    def tests_embedding_with_stub_vector_and_hashed_text(self):
        vendor = embeddings.EmbeddingVendor.FAKE
        model = embeddings.EmbeddingModel.FAKE
        service = embeddings.FakeEmbeddingService(vendor=vendor, model=model)

        embedding = service.get_embedding(text="some text")

        assert embedding.model == model
        assert embedding.vendor == vendor

        expected_vector = embeddings.get_stub_vector_embedding()
        np_testing.assert_array_equal(embedding.vector, expected_vector)
        assert embedding.embedded_content_hash == "552e21cd4cd9918678e3c1a0df491bc3"

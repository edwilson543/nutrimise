from nutrimise.domain import embeddings
from nutrimise.domain.embeddings._vendors import _fake


class TestGetEmbedding:
    def tests_embedding_with_stub_vector_and_hashed_text(self):
        vendor = embeddings.EmbeddingVendor.FAKE
        model = embeddings.EmbeddingModel.FAKE
        service = _fake.FakeEmbeddingService(vendor=vendor, model=model)

        embedding = service.get_embedding(text="some text")

        assert embedding.model == model
        assert embedding.vendor == vendor
        assert embedding.vector == service.stub_vector
        assert embedding.embedded_content_hash == "552e21cd4cd9918678e3c1a0df491bc3"

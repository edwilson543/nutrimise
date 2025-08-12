from nutrimise.domain import embeddings


class TestGetHashForText:
    def test_gets_expected_hash_for_text(self):
        text = "some text"

        hashed_text = embeddings.get_hash_for_text(text=text)

        assert hashed_text == "552e21cd4cd9918678e3c1a0df491bc3"
        assert embeddings.get_hash_for_text(text=text) == hashed_text

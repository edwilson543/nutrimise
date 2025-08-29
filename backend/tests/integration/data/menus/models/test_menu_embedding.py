import pytest
from django.db import IntegrityError

from testing.factories import data as data_factories


class TestUniqueConstraints:
    def test_raises_for_duplicate_embedding_for_model(self):
        embedding = data_factories.MenuEmbedding()

        with pytest.raises(IntegrityError):
            data_factories.MenuEmbedding(menu=embedding.menu, model=embedding.model)

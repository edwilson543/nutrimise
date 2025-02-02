import pytest
from django.db import IntegrityError

from tests.factories import data as data_factories


class TestUniqueConstraints:
    def test_raises_for_duplicate_embedding_for_model(self):
        embedding = data_factories.RecipeEmbedding()

        with pytest.raises(IntegrityError):
            data_factories.RecipeEmbedding(
                recipe=embedding.recipe, model=embedding.model
            )

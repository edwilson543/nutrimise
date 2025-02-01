import attrs
from django.db import models as django_models


EMBEDDING_DIMENSIONS = 1024


class EmbeddingVendor(django_models.TextChoices):
    OPEN_AI = "OPEN_AI"

    # Fakes.
    FAKE = "FAKE"
    FAKE_NO_SERVICE = "FAKE_NO_SERVICE"
    FAKE_NO_MODEL = "FAKE_NO_MODEL"


class EmbeddingModel(django_models.TextChoices):
    # OpenAI.
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"

    # Fakes.
    FAKE = "fake"


@attrs.frozen
class Embedding:
    embedding: list[float]
    vendor: EmbeddingVendor
    model: EmbeddingModel

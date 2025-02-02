import attrs
import numpy as np
from django.db import models as django_models


EMBEDDING_DIMENSIONS = 1024


class EmbeddingVendor(django_models.TextChoices):
    OPENAI = "OPENAI", "OpenAI"

    # Fakes.
    FAKE = "FAKE", "Fake"
    FAKE_NO_SERVICE = "FAKE_NO_SERVICE", "Fake no service"
    BROKEN = "BROKEN", "Broken"


class EmbeddingModel(django_models.TextChoices):
    # OpenAI.
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small", "text-embedding-3-small"

    # Fakes.
    FAKE = "fake", "fake"


@attrs.frozen
class Embedding:
    vector: np.ndarray = attrs.field(eq=attrs.cmp_using(eq=np.array_equal))
    embedded_content_hash: str
    vendor: EmbeddingVendor
    model: EmbeddingModel

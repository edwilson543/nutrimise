import attrs
import numpy as np
from django.db import models as django_models


EMBEDDING_DIMENSIONS = 3072


class EmbeddingVendor(django_models.TextChoices):
    OPENAI = "OPENAI", "OpenAI"

    # Fake vendors.
    FAKE = "FAKE", "Fake"
    FAKE_NO_SERVICE = "FAKE_NO_SERVICE", "Fake no service"
    BROKEN = "BROKEN", "Broken"


class EmbeddingModel(django_models.TextChoices):
    # OpenAI.
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small", "text-embedding-3-small"
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large", "text-embedding-3-large"

    # Fake models.
    FAKE = "fake", "fake"


@attrs.frozen
class Embedding:
    vector: np.ndarray = attrs.field(eq=attrs.cmp_using(eq=np.array_equal))
    prompt_hash: str
    vendor: EmbeddingVendor
    model: EmbeddingModel

from django.db import models as django_models
from pgvector import django as pgvector_django

from nutrimise.domain import embeddings

from . import _menu


class MenuEmbedding(django_models.Model):
    """
    The vector representation of a menu and its requirements, produced by an embedding model.
    """

    id = django_models.BigAutoField(primary_key=True)

    menu = django_models.ForeignKey(
        _menu.Menu, on_delete=django_models.CASCADE, related_name="embeddings"
    )

    vector = pgvector_django.VectorField(dimensions=embeddings.EMBEDDING_DIMENSIONS)

    embedded_content_hash = django_models.TextField()

    vendor = django_models.TextField(choices=embeddings.EmbeddingVendor.choices)

    model = django_models.TextField(choices=embeddings.EmbeddingModel.choices)

    class Meta:
        constraints = [
            django_models.UniqueConstraint(
                fields=["menu", "model"], name="unique_menu_embedding_per_model"
            )
        ]

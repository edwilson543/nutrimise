from django.db import models as django_models
from pgvector import django as pgvector_django

from nutrimise.domain import embeddings

from . import _recipe


class RecipeEmbedding(django_models.Model):
    """
    The vector representation of a recipe, produced by an embedding model.
    """

    id = django_models.BigAutoField(primary_key=True)

    recipe = django_models.ForeignKey(
        _recipe.Recipe, on_delete=django_models.CASCADE, related_name="embeddings"
    )

    vector = pgvector_django.VectorField(dimensions=embeddings.EMBEDDING_DIMENSIONS)

    embedded_content_hash = django_models.TextField()

    vendor = django_models.TextField(choices=embeddings.EmbeddingVendor.choices)

    model = django_models.TextField(choices=embeddings.EmbeddingModel.choices)

    class Meta:
        constraints = [
            django_models.UniqueConstraint(
                fields=["recipe", "model"], name="unique_recipe_embedding_per_model"
            )
        ]

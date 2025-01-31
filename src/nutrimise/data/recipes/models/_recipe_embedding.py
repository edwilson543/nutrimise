from django.db import models as django_models
from pgvector import django as pgvector_django

from nutrimise.data import constants

from . import _recipe


class RecipeEmbedding(django_models.Model):
    """
    The vector representation of a recipe, produced by an embedding model.
    """

    id = django_models.BigAutoField(primary_key=True)

    recipe = django_models.ForeignKey(
        _recipe.Recipe, on_delete=django_models.CASCADE, related_name="embeddings"
    )

    embedding = pgvector_django.VectorField(dimensions=constants.EMBEDDING_DIMENSIONS)

    vendor = django_models.TextField(choices=constants.EmbeddingVendor.choices)

    model = django_models.TextField(choices=constants.EmbeddingModel.choices)

    class Meta:
        constraints = [
            django_models.UniqueConstraint(
                fields=["recipe", "model"], name="unique_recipe_embedding_per_model"
            )
        ]

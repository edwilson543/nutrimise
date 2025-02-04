import django.db.models.deletion
import pgvector.django.vector
from django.db import migrations, models

from nutrimise.domain import embeddings


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RecipeEmbedding",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("vector", pgvector.django.vector.VectorField(dimensions=1024)),
                (
                    "model",
                    models.TextField(choices=embeddings.EmbeddingModel.choices),
                ),
                (
                    "vendor",
                    models.TextField(choices=embeddings.EmbeddingVendor.choices),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="embeddings",
                        to="recipes.recipe",
                    ),
                ),
                ("prompt_hash", models.TextField()),
            ],
        ),
        migrations.AddConstraint(
            model_name="recipeembedding",
            constraint=models.UniqueConstraint(
                fields=("recipe", "model"), name="unique_recipe_embedding_per_model"
            ),
        ),
    ]

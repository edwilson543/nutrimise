from django.core.management import base as django_management

from nutrimise.app import recipes as recipes_app
from nutrimise.data.recipes import models as recipe_models
from nutrimise.domain import embeddings


class Command(django_management.BaseCommand):
    """
    Backfill the embeddings for all recipes.
    """

    def handle(self, *args: object, **options: object) -> None:
        embedding_service = embeddings.get_embedding_service()

        for recipe_id in recipe_models.Recipe.objects.values_list("id", flat=True):
            try:
                recipes_app.create_or_update_recipe_embedding(
                    recipe_id=recipe_id, embedding_service=embedding_service
                )
            except recipes_app.UnableToGetEmbedding:
                continue

from . import models as menu_models
from nutrimise.domain import embeddings


def update_menu_item_recipe(*, menu_item_id: int, recipe_id: int) -> None:
    menu_item = menu_models.MenuItem.objects.get(id=menu_item_id)
    menu_item.update_recipe(recipe_id=recipe_id)


def create_or_update_menu_embedding(
    *, menu_id: int, embedding: embeddings.Embedding
) -> None:
    menu_models.MenuEmbedding.objects.update_or_create(
        menu_id=menu_id,
        model=embedding.model.value,
        vendor=embedding.vendor.value,
        defaults={
            "vector": embedding.vector,
            "embedded_content_hash": embedding.embedded_content_hash,
        },
    )

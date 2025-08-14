from nutrimise.domain import embeddings, menus

from . import models as menu_models


def update_menu_item_recipe(*, menu_item_id: int, recipe_id: int) -> None:
    menu_item = menu_models.MenuItem.objects.get(id=menu_item_id)
    menu_item.update_recipe(recipe_id=recipe_id)


def update_menu_requirements(
    *, menu_id: int, optimisation_mode: menus.OptimisationMode
) -> None:
    menu_models.MenuRequirements.objects.filter(menu_id=menu_id).update(
        optimisation_mode=optimisation_mode.value
    )


def create_or_update_menu_embedding(
    *, menu_id: int, embedding: embeddings.Embedding
) -> None:
    menu_models.MenuEmbedding.objects.update_or_create(
        menu_id=menu_id,
        model=embedding.model.value,
        vendor=embedding.vendor.value,
        defaults={
            "vector": embedding.vector,
            "prompt_hash": embedding.prompt_hash,
        },
    )

from nutrimise.data.menus import operations as menu_operations
from nutrimise.data.menus import queries as menu_queries
from nutrimise.domain import embeddings, menus


UnableToGetEmbedding = embeddings.UnableToGetEmbedding


def create_or_update_menu_embedding(
    *, menu_id: int, embedding_service: embeddings.EmbeddingService
) -> None:
    """
    Ensure the menu has an up-to-date embedding for the installed embedding service.

    raises UnableToGetEmbedding: If the service is unable to produce an embedding
        for some reason.
    """
    menu = menu_queries.get_menu(menu_id=menu_id)
    prompt = _get_prompt_for_menu(menu=menu)

    if _has_menu_already_been_embedded(
        menu=menu, prompt=prompt, embedding_service=embedding_service
    ):
        return

    embedding = embedding_service.get_embedding(text=prompt)
    menu_operations.create_or_update_menu_embedding(
        menu_id=menu_id, embedding=embedding
    )


def _get_prompt_for_menu(menu: menus.Menu) -> str:
    prompt = "Create an embedding of this menu that will be useful for comparing it with the embeddings of different recipes to see how well they match the requirements."
    prompt += f"\nMenu name: {menu.name}"
    if menu.description:
        prompt += f"\nMenu description: {menu.description}"
    return prompt


def _has_menu_already_been_embedded(
    *, menu: menus.Menu, prompt: str, embedding_service: embeddings.EmbeddingService
) -> bool:
    hashed_text = embeddings.get_hash_for_text(text=prompt)

    for embedding in menu.embeddings:
        if (
            embedding.vendor == embedding_service.vendor
            and embedding.model == embedding_service.model
            and embedding.prompt_hash == hashed_text
        ):
            return True

    return False

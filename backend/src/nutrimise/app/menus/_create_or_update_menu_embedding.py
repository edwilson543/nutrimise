from django import template as django_template

from nutrimise.data.menus import operations as menu_operations
from nutrimise.data.menus import queries as menu_queries
from nutrimise.domain import embeddings, menus


UnableToGetEmbedding = embeddings.UnableToGetEmbedding


def create_or_update_menu_embedding(
    *,
    menu_id: int,
    embedding_service: embeddings.EmbeddingService,
    user_prompt: str | None = None,
) -> None:
    """
    Ensure the menu has an up-to-date embedding for the installed embedding service.

    raises UnableToGetEmbedding: If the service is unable to produce an embedding
        for some reason.
    """
    menu = menu_queries.get_menu(menu_id=menu_id)
    prompt = _get_prompt_for_menu_embedding(menu=menu, user_prompt=user_prompt)

    if _has_menu_already_been_embedded(
        menu=menu, prompt=prompt, embedding_service=embedding_service
    ):
        return

    embedding = embedding_service.get_embedding(text=prompt)
    menu_operations.create_or_update_menu_embedding(
        menu_id=menu_id, embedding=embedding
    )


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


def _get_prompt_for_menu_embedding(menu: menus.Menu, *, user_prompt: str | None) -> str:
    template = django_template.Template(template_string=_PROMPT_TEMPLATE)
    context = django_template.Context({"menu": menu, "user_prompt": user_prompt})
    return template.render(context=context).rstrip()


_PROMPT_TEMPLATE = """Create an embedding of this meal plan: '{{ menu.name }}'.
The meal plan's embedding will be compared with the embeddings of different recipes, to see how well they match the meal plan's requirements.
{% if user_prompt %}The key requirement is to please the user, who has requested: '{{ user_prompt }}'{% endif %}
{% if menu.description %}The menu's description is: '{{ menu.description }}'{% endif %}
"""

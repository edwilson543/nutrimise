from django import template as django_template

from nutrimise.data.recipes import operations as recipe_operations
from nutrimise.data.recipes import queries as recipe_queries
from nutrimise.domain import embeddings, recipes


def create_or_update_recipe_embedding(
    *, recipe_id: int, embedding_service: embeddings.EmbeddingService
) -> None:
    """
    Ensure the recipe has an up-to-date embedding for the installed embedding service.

    raises UnableToGetEmbedding: If the service is unable to produce an embedding
        for some reason.
    """
    recipe = recipe_queries.get_recipe(recipe_id=recipe_id)
    prompt = _get_prompt_for_recipe_embedding(recipe=recipe)

    if _has_recipe_already_been_embedded(
        recipe=recipe, prompt=prompt, embedding_service=embedding_service
    ):
        return

    embedding = embedding_service.get_embedding(text=prompt)
    recipe_operations.create_or_update_recipe_embedding(
        recipe_id=recipe_id, embedding=embedding
    )


def _has_recipe_already_been_embedded(
    *,
    recipe: recipes.Recipe,
    prompt: str,
    embedding_service: embeddings.EmbeddingService,
) -> bool:
    hashed_prompt = embeddings.get_hash_for_text(text=prompt)

    for embedding in recipe.embeddings:
        if (
            embedding.vendor == embedding_service.vendor
            and embedding.model == embedding_service.model
            and embedding.prompt_hash == hashed_prompt
        ):
            return True

    return False


def _get_prompt_for_recipe_embedding(*, recipe: recipes.Recipe) -> str:
    template = django_template.Template(template_string=_PROMPT_TEMPLATE)
    context = django_template.Context({"recipe": recipe})
    return template.render(context=context).rstrip()


_PROMPT_TEMPLATE = """Create an embedding of this recipe that will be useful for:
- Sematic search
- Comparing it with the embeddings of meal plan requirements

Name: {{ recipe.name }}
{% if recipe.description %}Description: {{ recipe.description }}{% endif %}
{% if recipe.methodology %}Methodology: {{ recipe.methodology }}{% endif %}
{% for ingredient in recipe.ingredients %}{% if forloop.first %}Ingredients:{% endif %}
- {{ ingredient.ingredient.name }}
{% endfor %}"""

from django.template import loader as django_template_loader

from nutrimise.domain import recipes


def get_prompt_for_recipe_embedding(*, recipe: recipes.Recipe) -> str:
    template = django_template_loader.get_template("recipe-embedding.txt")

    context = {"recipe": recipe}
    return template.render(context=context).rstrip()

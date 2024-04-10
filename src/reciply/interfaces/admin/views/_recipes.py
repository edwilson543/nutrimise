# Standard library imports
from typing import Any

# Django imports
from django import http

# Local application imports
from reciply.data.recipes import models as recipe_models
from reciply.domain import ingredients

from . import _base


class RecipeDetails(_base.AdminTemplateView):
    template_name = "admin/recipes/recipe-details.html"

    recipe: recipe_models.Recipe

    def setup(self, request: http.HttpRequest, *args: object, **kwargs: int) -> None:
        super().setup(request, *args, **kwargs)
        self.recipe = recipe_models.Recipe.objects.get(id=kwargs["recipe_id"])

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["recipe"] = self.recipe
        context["recipe_ingredients"] = list(self.recipe.ingredients.all())
        context["nutritional_information"] = (
            ingredients.get_nutritional_information_for_recipe(
                recipe=self.recipe, per_serving=True
            )
        )
        return context

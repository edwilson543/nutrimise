from typing import Any

from django import http

from nutrimise.data.recipes import models as recipe_models
from nutrimise.domain import ingredients

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
        recipe_ingredients = self.recipe.ingredients.order_by(
            "ingredient__category__name", "ingredient__name"
        )
        context["recipe_ingredients"] = list(recipe_ingredients)
        context["nutritional_information"] = (
            ingredients.get_nutritional_information_for_recipe(
                recipe=self.recipe, per_serving=True
            )
        )
        return context

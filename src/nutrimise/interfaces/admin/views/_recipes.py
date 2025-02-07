from typing import Any

from django import forms as django_forms
from django import http
from django import urls as django_urls
from django.contrib import messages
from PIL import Image

from nutrimise.app import recipes as recipes_app
from nutrimise.data.ingredients import queries as ingredient_queries
from nutrimise.data.recipes import models as recipe_models
from nutrimise.domain import image_extraction

from . import _base, _types


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
            ingredient_queries.get_nutritional_information_for_recipe(
                recipe=self.recipe, per_serving=True
            )
        )
        return context


class TempExtractionView(_base.AdminFormView):
    class ImageUpload(django_forms.Form):
        image = django_forms.ImageField()

    form_class = ImageUpload
    template_name = "admin/recipes/extract-recipe.html"

    request: _types.AuthenticatedHttpRequest
    _recipe_id: int

    def form_valid(self, form: ImageUpload) -> http.HttpResponse:
        service = image_extraction.get_image_extraction_service()
        uploaded_image = Image.open(form.cleaned_data["image"])
        self._recipe_id = recipes_app.extract_recipe_from_image(
            uploaded_image=uploaded_image,
            image_extraction_service=service,
            author=self.request.user,
        )

        message = "Recipe was successfully extracted"
        messages.success(request=self.request, message=message)

        return super().form_valid(form=form)

    def get_success_url(self) -> str:
        return django_urls.reverse(
            "admin:recipes_recipe_change", kwargs={"object_id": self._recipe_id}
        )

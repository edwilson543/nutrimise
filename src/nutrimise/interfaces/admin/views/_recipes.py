from typing import Any

from django import http, shortcuts
from django import urls as django_urls
from django.contrib import messages as django_messages
from PIL import Image

from nutrimise.app import recipes as recipes_app
from nutrimise.data.ingredients import queries as ingredient_queries
from nutrimise.data.recipes import models as recipe_models
from nutrimise.domain import image_extraction
from nutrimise.interfaces.admin import forms

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


class ExtractRecipeFromImage(_base.AdminFormView):
    form_class = forms.ImageUpload
    http_method_names = ["post"]

    # Instance attributes.
    request: _types.AuthenticatedHttpRequest
    _recipe_id: int
    _image_extraction_service: image_extraction.ImageExtractionService

    def dispatch(
        self, request: http.HttpRequest, *args: object, **kwargs: object
    ) -> http.HttpResponseBase:
        try:
            self._image_extraction_service = (
                image_extraction.get_image_extraction_service()
            )
        except image_extraction.ImageExtractionServiceMisconfigured:
            return self._error_response(
                error_message="Image extraction is not configured."
            )

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: forms.ImageUpload) -> http.HttpResponse:
        uploaded_image = Image.open(form.cleaned_data["image"])

        try:
            self._recipe_id = recipes_app.extract_recipe_from_image(
                uploaded_image=uploaded_image,
                image_extraction_service=self._image_extraction_service,
                author=None,
            )
        except image_extraction.UnableToExtractRecipeFromImage:
            return self._error_response(
                error_message="Unexpected error extracting image from recipe."
            )

        message = "Recipe was successfully extracted"
        django_messages.success(request=self.request, message=message)

        return super().form_valid(form=form)

    def form_invalid(self, form: forms.ImageUpload) -> http.HttpResponse:
        return self._error_response(error_message=form.errors.as_text())

    def get_success_url(self) -> str:
        return django_urls.reverse(
            "admin:recipes_recipe_change", kwargs={"object_id": self._recipe_id}
        )

    def _error_response(self, error_message: str) -> http.HttpResponse:
        django_messages.error(request=self.request, message=error_message)
        redirect_url = django_urls.reverse("admin:recipes_recipe_add")
        return shortcuts.redirect(redirect_url)

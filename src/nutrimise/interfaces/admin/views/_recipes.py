from typing import Any

from django import http, shortcuts
from django import urls as django_urls
from django.contrib import messages as django_messages
from PIL import Image

from nutrimise.app import recipes as recipes_app
from nutrimise.data.ingredients import queries as ingredient_queries
from nutrimise.data.recipes import models as recipe_models
from nutrimise.domain import data_extraction, embeddings
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


class _ExtractRecipe(_base.AdminFormView):
    http_method_names = ["post"]

    # Instance attributes.
    request: _types.AuthenticatedHttpRequest
    _recipe_id: int
    _data_extraction_service: data_extraction.DataExtractionService
    _embedding_service: embeddings.EmbeddingService

    def dispatch(
        self, request: http.HttpRequest, *args: object, **kwargs: object
    ) -> http.HttpResponseBase:
        try:
            self._data_extraction_service = (
                data_extraction.get_data_extraction_service()
            )
        except data_extraction.DataExtractionServiceMisconfigured:
            return self._error_response(
                error_message="Image extraction service is not configured."
            )

        try:
            self._embedding_service = embeddings.get_embedding_service()
        except embeddings.EmbeddingServiceMisconfigured:
            return self._error_response(
                error_message="Embedding service is not configured."
            )

        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form: forms.ExtractRecipeFromImage) -> http.HttpResponse:
        return self._error_response(error_message=form.errors.as_text())

    def get_success_url(self) -> str:
        return django_urls.reverse(
            "admin:recipes_recipe_change", kwargs={"object_id": self._recipe_id}
        )

    def _error_response(self, error_message: str) -> http.HttpResponse:
        django_messages.error(request=self.request, message=error_message)
        redirect_url = django_urls.reverse("admin:recipes_recipe_add")
        return shortcuts.redirect(redirect_url)


class ExtractRecipeFromImage(_ExtractRecipe):
    form_class = forms.ExtractRecipeFromImage

    def form_valid(self, form: forms.ExtractRecipeFromImage) -> http.HttpResponse:
        uploaded_image = Image.open(form.cleaned_data["image"])

        try:
            self._recipe_id = recipes_app.extract_recipe_from_image(
                author=form.cleaned_data.get("author"),
                image=uploaded_image,
                data_extraction_service=self._data_extraction_service,
                embedding_service=self._embedding_service,
            )
        except data_extraction.UnableToExtractRecipe:
            return self._error_response(
                error_message="Unexpected error extracting recipe from image."
            )

        message = "Recipe was successfully extracted"
        django_messages.success(request=self.request, message=message)

        return super().form_valid(form=form)


class ExtractRecipeFromURL(_ExtractRecipe):
    form_class = forms.ExtractRecipeFromURL

    def form_valid(self, form: forms.ExtractRecipeFromURL) -> http.HttpResponse:
        try:
            self._recipe_id = recipes_app.extract_recipe_from_url(
                url=form.cleaned_data["url"],
                data_extraction_service=self._data_extraction_service,
                embedding_service=self._embedding_service,
            )
        except data_extraction.UnableToExtractRecipe:
            return self._error_response(
                error_message="Unexpected error extracting recipe from url."
            )

        message = "Recipe was successfully extracted"
        django_messages.success(request=self.request, message=message)

        return super().form_valid(form=form)

    def form_invalid(self, form: forms.ExtractRecipeFromImage) -> http.HttpResponse:
        return self._error_response(error_message=form.errors.as_text())

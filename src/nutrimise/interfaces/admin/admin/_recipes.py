from django import forms as django_forms
from django import http as django_http
from django import urls as django_urls
from django.contrib import admin
from django.db import models as django_models
from django.utils import safestring

from nutrimise.app import recipes as recipes_app
from nutrimise.data.recipes import models as recipe_models
from nutrimise.data.recipes import queries as recipe_queries
from nutrimise.domain import embeddings


class _RecipeIngredientInline(admin.TabularInline):
    model = recipe_models.RecipeIngredient
    extra = 10


@admin.register(recipe_models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "author", "user_actions"]
    list_display_links = ["name"]
    ordering = ["name"]
    search_fields = ["name"]

    inlines = [
        _RecipeIngredientInline,
    ]

    @admin.display(description="Actions")
    def user_actions(self, recipe: recipe_models.Recipe) -> safestring.SafeString:
        detail_url = django_urls.reverse(
            "recipe-details", kwargs={"recipe_id": recipe.id}
        )
        edit_url = django_urls.reverse(
            "admin:recipes_recipe_change", kwargs={"object_id": recipe.id}
        )
        return safestring.mark_safe(
            f'<a href="{detail_url}"><b>View</b></a> | <a href="{edit_url}"><b>Edit</b></a>'
        )

    def save_model(
        self,
        request: django_http.HttpRequest,
        obj: recipe_models.Recipe,
        form: django_forms.ModelForm,
        change: bool,
    ) -> None:
        super().save_model(request=request, obj=obj, form=form, change=change)
        recipes_app.create_or_update_recipe_embedding(
            recipe_id=obj.id, embedding_service=embeddings.get_embedding_service()
        )

    def get_search_results(
        self,
        request: django_http.HttpRequest,
        queryset: django_models.QuerySet[recipe_models.Recipe],
        search_term: str,
    ) -> tuple[django_models.QuerySet[recipe_models.Recipe], bool]:
        """
        Use embeddings to perform a semantic search of the recipe library.

        raises UnableToGetEmbedding: If the service is unable to produce an embedding
            for the search text some reason.
        """
        if not search_term:
            return super().get_search_results(
                request=request, queryset=queryset, search_term=search_term
            )

        embedding_service = embeddings.get_embedding_service()
        search_embedding = embedding_service.get_embedding(text=search_term)
        results = recipe_queries.get_recipes_closest_to_vector(
            embedding=search_embedding, limit=5
        )
        return results, False


@admin.register(recipe_models.RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ["id", "recipe_name", "ingredient_name", "quantity", "units"]
    ordering = ["recipe__name", "ingredient__name"]

    @admin.display(description="Recipe name")
    def recipe_name(self, ingredient: recipe_models.RecipeIngredient) -> str:
        return ingredient.recipe.name

    @admin.display(description="Ingredient name")
    def ingredient_name(self, ingredient: recipe_models.RecipeIngredient) -> str:
        return ingredient.ingredient.name

    @admin.display(description="Units")
    def units(self, ingredient: recipe_models.RecipeIngredient) -> str:
        return ingredient.ingredient.units or "No units"


@admin.register(recipe_models.RecipeEmbedding)
class RecipeEmbeddingAdmin(admin.ModelAdmin):
    list_display = [
        "vendor",
        "model",
        "prompt_hash",
        "vector_length",
        "recipe_name",
    ]
    list_display_links = ["prompt_hash"]
    ordering = ["recipe__name"]

    @admin.display(description="Recipe name")
    def recipe_name(self, embedding: recipe_models.RecipeEmbedding) -> str:
        return embedding.recipe.name

    @admin.display(description="Vector length")
    def vector_length(self, embedding: recipe_models.RecipeEmbedding) -> int:
        return len(embedding.vector)

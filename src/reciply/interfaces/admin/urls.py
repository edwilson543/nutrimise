from django import urls as django_urls

from . import views

urlpatterns = [
    django_urls.path(
        route="recipes/<int:recipe_id>/",
        view=views.RecipeDetails.as_view(),
        name="recipe-details",
    )
]

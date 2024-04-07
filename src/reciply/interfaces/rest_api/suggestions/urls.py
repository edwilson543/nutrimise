# Django imports
from django import urls as django_urls

from . import views

urlpatterns = [
    django_urls.path(
        "recipes/for-menu/<int:id>/",
        views.SuggestRecipesForMenu.as_view(),
        name="suggest-recipes-for-menu",
    ),
]

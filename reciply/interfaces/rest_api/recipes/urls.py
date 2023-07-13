# Django imports
from django import urls as django_urls

from . import views

urlpatterns = [
    django_urls.path(
        "recipe/list/", views.MyRecipeList.as_view(), name="my-recipe-list"
    )
]

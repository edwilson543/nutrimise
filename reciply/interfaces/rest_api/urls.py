# Third party imports
from knox import views as knox_views

# Django imports
from django import urls

from .users import views as user_views

urlpatterns = [
    # ----------
    # Auth
    # ----------
    urls.path("login/", user_views.Login.as_view(), name="login"),
    urls.path("logout/", knox_views.LogoutView.as_view(), name="logout"),
    urls.path("logout-all/", knox_views.LogoutAllView.as_view(), name="logout-all"),
    # ----------
    # Recipes
    # ----------
    urls.path("recipes/", urls.include("interfaces.rest_api.recipes.urls")),
]

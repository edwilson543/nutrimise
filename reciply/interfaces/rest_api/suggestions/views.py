# Third party imports
from rest_framework import response
from rest_framework import status as drf_status
from rest_framework import views

# Django imports
from django import shortcuts

# Local application imports
from data.menus import models as menu_models
from domain.suggestions.recipes import suggest as suggest_recipes
from interfaces.rest_api import types
from interfaces.rest_api.recipes import serializers


class SuggestRecipesForMenu(views.APIView):
    """
    Suggest some recipes for a user decide whether to add to a menu.
    """

    http_method_names = ["get"]

    def get(
        self, request: types.AuthenticatedRequest, *args: object, **kwargs: object
    ) -> response.Response:
        menu = shortcuts.get_object_or_404(
            klass=menu_models.Menu, id=kwargs["id"], author=request.user
        )
        recipes = suggest_recipes.get_suggested_recipes_for_menu(menu=menu)
        serialized_recipes = serializers.RecipeList(instance=recipes, many=True).data
        return response.Response(serialized_recipes, status=drf_status.HTTP_200_OK)

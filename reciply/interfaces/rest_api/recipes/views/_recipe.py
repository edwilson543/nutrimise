# Third party imports
from rest_framework import response
from rest_framework import status as drf_status
from rest_framework import views

# Django imports
from django import shortcuts

# Local application imports
from data.recipes import models as recipe_models
from domain.recipes import queries
from interfaces.rest_api import types
from interfaces.rest_api.recipes import serializers


class MyRecipeList(views.APIView):
    """
    Get all the recipes that the user has written.
    """

    http_method_names = ["get"]

    def get(
        self, request: types.AuthenticatedRequest, *args: object, **kwargs: object
    ) -> response.Response:
        recipes = queries.get_recipes_authored_by_user(author=request.user)
        serialized_recipes = serializers.Recipe(instance=recipes, many=True).data
        return response.Response(serialized_recipes, status=drf_status.HTTP_200_OK)


class RecipeDetail(views.APIView):
    """
    Get the details for a single recipe.
    """

    http_method_names = ["get"]

    def get(
        self, request: types.AuthenticatedRequest, *args: object, **kwargs: object
    ) -> response.Response:
        recipe = shortcuts.get_object_or_404(
            klass=recipe_models.Recipe, id=kwargs["id"], author=request.user
        )
        serialized_recipes = serializers.Recipe(instance=recipe).data
        return response.Response(serialized_recipes, status=drf_status.HTTP_200_OK)

# Third party imports
from rest_framework import response
from rest_framework import status as drf_status
from rest_framework import views

# Local application imports
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

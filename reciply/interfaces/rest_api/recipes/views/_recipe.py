# Third party imports
from rest_framework import response
from rest_framework import status as drf_status
from rest_framework import views

# Django imports
from django import shortcuts

# Local application imports
from app import recipes
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
        recipes = queries.get_recipes_authored_by_user(
            author=request.user
        ).prefetch_related("images")
        serialized_recipes = serializers.RecipeList(instance=recipes, many=True).data
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
        serialized_recipes = serializers.RecipeDetail(instance=recipe).data
        return response.Response(serialized_recipes, status=drf_status.HTTP_200_OK)


class RecipeCreate(views.APIView):
    """
    Create a new recipe.
    """

    http_method_names = ["post"]

    def post(
        self, request: types.AuthenticatedRequest, *args: object, **kwargs: object
    ) -> response.Response:
        serializer = serializers.RecipeCreate(data=request.data)
        if serializer.is_valid():
            try:
                recipe = recipes.create_recipe(
                    author=request.user,
                    name=serializer.validated_data["name"],
                    description=serializer.validated_data["description"],
                )
            except recipes.RecipeNameNotUniqueForAuthor:
                errors = {"name": "You already have a recipe with this name!"}
                return response.Response(errors, status=drf_status.HTTP_400_BAD_REQUEST)

            response_data = serializers.RecipeCreate(instance=recipe).data
            return response.Response(response_data, status=drf_status.HTTP_201_CREATED)

        return response.Response(
            serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST
        )

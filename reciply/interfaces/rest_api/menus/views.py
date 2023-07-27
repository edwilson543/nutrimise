# Third party imports
from rest_framework import response
from rest_framework import status as drf_status
from rest_framework import views

# Django imports
from django import shortcuts

# Local application imports
from app import menus
from data.menus import models as menu_models
from domain.menus import queries
from interfaces.rest_api import types
from interfaces.rest_api.menus import serializers


class MyMenuList(views.APIView):
    """
    Get all the menus that the user has written.
    """

    http_method_names = ["get"]

    def get(
        self, request: types.AuthenticatedRequest, *args: object, **kwargs: object
    ) -> response.Response:
        menus = (
            queries.get_menus_authored_by_user(author=request.user)
            .prefetch_related("items")
            .order_by("name")
        )
        serialized_menus = serializers.MenuList(instance=menus, many=True).data
        return response.Response(serialized_menus, status=drf_status.HTTP_200_OK)


class MenuDetail(views.APIView):
    """
    Get the details for a single menu.
    """

    http_method_names = ["get"]

    def get(
        self, request: types.AuthenticatedRequest, *args: object, **kwargs: object
    ) -> response.Response:
        menu = shortcuts.get_object_or_404(
            klass=menu_models.Menu, id=kwargs["id"], author=request.user
        )
        serialized_menus = serializers.MenuDetail(instance=menu).data
        return response.Response(serialized_menus, status=drf_status.HTTP_200_OK)


class MenuCreate(views.APIView):
    """
    Create a new menu.
    """

    http_method_names = ["post"]

    def post(
        self, request: types.AuthenticatedRequest, *args: object, **kwargs: object
    ) -> response.Response:
        serializer = serializers.MenuCreate(data=request.data)
        if serializer.is_valid():
            try:
                menu = menus.create_menu(
                    author=request.user,
                    name=serializer.validated_data["name"],
                    description=serializer.validated_data["description"],
                )
            except menus.MenuNameNotUniqueForAuthor:
                errors = {"name": ["You already have a menu with this name!"]}
                return response.Response(errors, status=drf_status.HTTP_400_BAD_REQUEST)

            response_data = serializers.MenuCreate(instance=menu)
            return response.Response(
                response_data.data, status=drf_status.HTTP_201_CREATED
            )

        return response.Response(
            serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST
        )


class AddItemsToMenu(views.APIView):
    """
    Add some recipes to a menu at a specific day and meal time.
    """

    http_method_names = ["post"]

    def post(
        self, request: types.AuthenticatedRequest, *args: object, **kwargs: object
    ) -> response.Response:
        menu = shortcuts.get_object_or_404(
            klass=menu_models.Menu, id=kwargs["id"], author=request.user
        )
        serializer = serializers.AddItemsToMenu(data=request.data, many=True)
        if serializer.is_valid():
            try:
                menu_items = menus.add_items_to_menu(
                    menu=menu, items=serializer.validated_data
                )
            except menus.MealTimesAreNotUnique:
                errors = {
                    "items": ["You cannot select more than one recipe per meal time!"]
                }
                return response.Response(errors, status=drf_status.HTTP_400_BAD_REQUEST)

            response_data = serializers.AddItemsToMenu(instance=menu_items, many=True)
            return response.Response(
                response_data.data, status=drf_status.HTTP_201_CREATED
            )

        return response.Response(
            serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST
        )

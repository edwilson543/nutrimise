# Third party imports
# Third party imports
from rest_framework import response
from rest_framework import status as drf_status
from rest_framework import views

# Django imports
from django import shortcuts

# Local application imports
from reciply.app import menus as menus_app
from reciply.data.menus import models as menu_models
from reciply.domain import menus
from reciply.interfaces.rest_api import types
from reciply.interfaces.rest_api.menus import serializers


class MyMenuList(views.APIView):
    """
    Get all the menus that the user has written.
    """

    http_method_names = ["get"]

    def get(
        self, request: types.AuthenticatedRequest, *args: object, **kwargs: object
    ) -> response.Response:
        users_menus = (
            menus.get_menus_authored_by_user(author=request.user)
            .prefetch_related("items")
            .order_by("name")
        )
        serialized_menus = serializers.MenuList(instance=users_menus, many=True).data
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
                menu = menus_app.create_menu(
                    author=request.user,
                    name=serializer.validated_data["name"],
                    description=serializer.validated_data.get("description", ""),
                    add_suggestions=serializer.validated_data["add_suggestions"],
                )
            except menus_app.MenuNameNotUniqueForAuthor:
                errors = {"name": ["You already have a menu with this name!"]}
                return response.Response(errors, status=drf_status.HTTP_400_BAD_REQUEST)

            response_data = serializers.MenuDetail(instance=menu)
            return response.Response(
                response_data.data, status=drf_status.HTTP_201_CREATED
            )

        return response.Response(
            serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST
        )


class AddItemToMenu(views.APIView):
    """
    Add a recipe to a menu for a specific meal time and day.
    """

    http_method_names = ["post"]

    def post(
        self, request: types.AuthenticatedRequest, *args: object, **kwargs: object
    ) -> response.Response:
        menu = shortcuts.get_object_or_404(
            klass=menu_models.Menu, id=kwargs["id"], author=request.user
        )
        serializer = serializers.AddItemToMenu(data=request.data)
        if serializer.is_valid():
            menu_item = menus_app.add_item_to_menu(
                menu=menu,
                recipe_id=serializer.validated_data["recipe_id"],
                day=serializer.validated_data["day"],
                meal_time=serializer.validated_data["meal_time"],
            )
            response_data = serializers.MenuItem(instance=menu_item)
            return response.Response(
                response_data.data, status=drf_status.HTTP_201_CREATED
            )

        return response.Response(
            serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST
        )


class AddItemsToMenu(views.APIView):
    """
    Add some recipes to a menu for some specific days and meal times.
    """

    http_method_names = ["post"]

    def post(
        self, request: types.AuthenticatedRequest, *args: object, **kwargs: object
    ) -> response.Response:
        menu = shortcuts.get_object_or_404(
            klass=menu_models.Menu, id=kwargs["id"], author=request.user
        )
        serializer = serializers.AddItemToMenu(data=request.data, many=True)
        if serializer.is_valid():
            try:
                menu_items = menus_app.add_items_to_menu(
                    menu=menu, items=serializer.validated_data
                )
            except menus_app.MealTimesAreNotUnique:
                errors = {
                    "items": ["You cannot select more than one recipe per meal time!"]
                }
                return response.Response(errors, status=drf_status.HTTP_400_BAD_REQUEST)

            response_data = serializers.AddItemToMenu(instance=menu_items, many=True)
            return response.Response(
                response_data.data, status=drf_status.HTTP_201_CREATED
            )

        return response.Response(
            serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST
        )


class MenuItem(views.APIView):
    """
    Remove an item from a menu.
    """

    http_method_names = ["delete"]

    def delete(
        self, request: types.AuthenticatedRequest, *args: object, **kwargs: object
    ) -> response.Response:
        menu_item = shortcuts.get_object_or_404(
            klass=menu_models.MenuItem, id=kwargs["id"], menu__author=request.user
        )
        menus_app.delete_menu_item(item=menu_item)
        return response.Response(status=drf_status.HTTP_200_OK)


class GenerateShoppingList(views.APIView):
    """
    Generate a shopping list for a menu.
    """

    http_method_names = ["get"]

    def get(
        self, request: types.AuthenticatedRequest, *args: object, **kwargs: object
    ) -> response.Response:
        menu = shortcuts.get_object_or_404(
            klass=menu_models.Menu, id=kwargs["id"], author=request.user
        )
        shopping_list = menus_app.generate_shopping_list(menu=menu)
        return response.Response(shopping_list, status=drf_status.HTTP_200_OK)

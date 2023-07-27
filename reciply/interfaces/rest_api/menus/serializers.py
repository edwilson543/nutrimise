# Standard library imports
import typing

# Third party imports
from rest_framework import serializers
from rest_framework.utils import serializer_helpers

# Local application imports
from data import constants
from data.menus import models as menu_models
from interfaces.rest_api.recipes import serializers as recipe_serializers


class _MenuBase(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=128)
    description = serializers.CharField()


class _MenuItem(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    recipe = recipe_serializers.RecipeList()
    day = serializers.ChoiceField(choices=constants.Day.choices)
    meal_time = serializers.ChoiceField(choices=constants.MealTime.choices)


class MenuList(_MenuBase):
    number_of_items = serializers.SerializerMethodField()

    def get_number_of_items(self, menu: menu_models.Menu) -> int:
        return menu.items.count()


class MenuDetail(MenuList):
    items = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_items(self, menu: menu_models.Menu) -> list[serializer_helpers.ReturnDict]:
        items = menu.items.select_related("recipe").order_by("day")
        return typing.cast(
            list[serializer_helpers.ReturnDict],
            _MenuItem(instance=items, many=True).data,
        )


class MenuCreate(_MenuBase):
    pass


class AddItemToMenu(_MenuItem):
    menu_id = serializers.IntegerField(min_value=1)
    recipe_id = serializers.IntegerField(min_value=1)
    day = serializers.ChoiceField(choices=constants.Day.choices)
    meal_time = serializers.ChoiceField(choices=constants.MealTime.choices)

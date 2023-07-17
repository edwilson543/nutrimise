# Third party imports
from rest_framework import serializers

# Django imports
from django.conf import settings

# Local application imports
from data.recipes import models as recipe_models


class Recipe(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=128)
    description = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class RecipeImage(serializers.Serializer):
    image_source = serializers.SerializerMethodField()
    is_hero = serializers.BooleanField()

    def get_image_source(self, recipe_image: recipe_models.RecipeImage) -> str:
        return settings.MEDIA_BASE_URL + recipe_image.image.url

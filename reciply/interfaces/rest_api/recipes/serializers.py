# Third party imports
from rest_framework import serializers

# Django imports
from django.conf import settings

# Local application imports
from data.recipes import models as recipe_models
from domain.recipes import queries


class _RecipeBase(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=128)
    description = serializers.CharField()


class RecipeImage(serializers.Serializer):
    image_source = serializers.SerializerMethodField()
    is_hero = serializers.BooleanField()

    def get_image_source(self, recipe_image: recipe_models.RecipeImage) -> str:
        return settings.MEDIA_BASE_URL + recipe_image.image.url


class RecipeList(_RecipeBase):
    hero_image_source = serializers.SerializerMethodField(read_only=True)

    def get_hero_image_source(self, recipe: recipe_models.Recipe) -> str | None:
        if image := queries.get_hero_image(recipe):
            return settings.MEDIA_BASE_URL + image.image.url
        return None


class RecipeDetail(RecipeList):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class RecipeCreate(_RecipeBase):
    hero_image = serializers.ImageField(required=False)

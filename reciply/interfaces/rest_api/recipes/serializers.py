# Third party imports
from rest_framework import serializers


class Recipe(serializers.Serializer):
    id = serializers.IntegerField()
    author = serializers.ImageField()
    name = serializers.CharField(max_length=128)
    description = serializers.CharField()

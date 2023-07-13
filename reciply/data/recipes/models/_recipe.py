# Django imports
from django.contrib.auth import models as auth_models
from django.db import models as django_models

# Local application imports
from data import constants


class Recipe(django_models.Model):
    """
    Basic data that defines a recipe.
    """

    id = django_models.AutoField(primary_key=True)

    author = django_models.ForeignKey(auth_models.User, on_delete=django_models.CASCADE)

    name = django_models.CharField(max_length=128)

    description = django_models.TextField()

    image = django_models.ImageField(
        null=True, upload_to=constants.MediaNamespace.RECIPES
    )

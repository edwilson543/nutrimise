from django.db import models as django_models


class DietaryRequirement(django_models.Model):
    """
    Some dietary requirement.
    """

    id = django_models.AutoField(primary_key=True)

    name = django_models.TextField(unique=True)

    def __str__(self) -> str:
        return self.name

# Standard library imports
from typing import Any

# Third party imports
import factory

# Django imports
from django.contrib.auth import models as auth_models


class User(factory.django.DjangoModelFactory):
    username = factory.Faker("user_name")
    password = factory.Faker("password")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.lazy_attribute(lambda obj: obj.first_name + "@test.com")

    class Meta:
        model = auth_models.User

    @classmethod
    def create(cls, **kwargs: object) -> dict[str, Any]:
        return auth_models.User.objects.create_user(**kwargs)

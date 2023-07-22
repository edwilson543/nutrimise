# Third party imports
import factory
from knox import models as knox_models

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
    def _create(
        cls, model_class: type[auth_models.User], *args: object, **kwargs: object
    ) -> auth_models.User:
        """
        Use create_user so that the password can be manually set.
        """
        return model_class.objects.create_user(*args, **kwargs)


class AuthToken(factory.django.DjangoModelFactory):
    user = factory.SubFactory(User)

    class Meta:
        model = knox_models.AuthToken

    @classmethod
    def create(cls, **kwargs: object) -> tuple[knox_models.AuthToken, str]:
        user = kwargs.get("user") or User()
        return knox_models.AuthToken.objects.create(user=user)

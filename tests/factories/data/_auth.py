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
    def _create(
        cls, model_class: type[auth_models.User], *args: object, **kwargs: object
    ) -> auth_models.User:
        """
        Use create_user so that the password can be manually set.
        """
        return model_class.objects.create_user(*args, **kwargs)

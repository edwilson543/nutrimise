# Django imports
from django.contrib.auth import models as auth_models
from django.db import models as django_models

# Local application imports
from data.menus import models as menu_models


def get_menus_authored_by_user(
    author: auth_models.User,
) -> django_models.QuerySet[menu_models.Menu]:
    return menu_models.Menu.objects.filter(author=author)

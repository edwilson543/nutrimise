# Standard library imports
import datetime as dt
from typing import TypedDict

# Third party imports
from knox import models as knox_models

# Django imports
from django import db as django_db
from django.contrib.auth import models as auth_models
from django.db import transaction


class Token(TypedDict):
    expiry: dt.datetime | None
    token: str


class UserAlreadyExists(django_db.IntegrityError):
    pass


@transaction.atomic
def create_user(*, username: str, password: str, email: str) -> Token:
    try:
        user = auth_models.User.objects.create_user(
            username=username, password=password, email=email
        )
    except django_db.IntegrityError:
        raise UserAlreadyExists
    instance, token = knox_models.AuthToken.objects.create(user=user)
    return {"expiry": instance.expiry, "token": token}

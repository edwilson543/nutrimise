# Standard library imports
from unittest import mock

# Third party imports
import pytest
from knox import crypto
from knox import models as knox_models

# Django imports
from django.contrib.auth import models as auth_models

# Local application imports
from app.users import _create_user
from tests import factories


class TestCreateUser:
    def test_creates_user_and_token(self):
        token_data = _create_user.create_user(
            username="username", password="password", email="test@example.com"
        )

        assert token_data == {"expiry": None, "token": mock.ANY}

        user = auth_models.User.objects.get()
        assert user.username == "username"
        assert user.email == "test@example.com"

        token = knox_models.AuthToken.objects.get()
        assert token.user == user
        digest = crypto.hash_token(token_data["token"])
        assert token.digest == digest

    def test_raises_for_duplicated_username(self):
        user = factories.User()

        with pytest.raises(_create_user.UserAlreadyExists):
            _create_user.create_user(
                username=user.username, password="password", email="test@example.com"
            )

# Standard library imports
from unittest import mock

# Third party imports
from knox import models as knox_models
from rest_framework import status

# Django imports
from django import urls as django_urls
from django.contrib.auth import models as auth_models


class TestRegister:
    def test_user_with_valid_username_and_password_can_login(self, rest_api_client):
        data = {
            "username": "username",
            "password1": "password",
            "password2": "password",
            "email": "test@example.com",
        }

        register_url = django_urls.reverse("register")
        response = rest_api_client.post(register_url, data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"expiry": None, "token": mock.ANY}

        user = auth_models.User.objects.get()
        assert user.username == "username"
        assert user.auth_token_set.exists()

    def test_non_matching_passwords_bad_response(self, rest_api_client):
        data = {
            "username": "username",
            "password1": "password",
            "password2": "different-password",
            "email": "test@example.com",
        }

        register_url = django_urls.reverse("register")
        response = rest_api_client.post(register_url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"password": ["Passwords do not match"]}

        assert not auth_models.User.objects.exists()
        assert not knox_models.AuthToken.objects.exists()

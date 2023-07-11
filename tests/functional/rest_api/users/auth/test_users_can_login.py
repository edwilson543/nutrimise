# Standard library imports
import base64
from unittest import mock

# Third party imports
from knox import models as knox_models
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework import exceptions as drf_exceptions
from rest_framework import status

# Django imports
from django import urls as django_urls

# Local application imports
from tests import factories


class TestLogin:
    def test_user_with_valid_username_and_password_can_login(self, rest_api_client):
        username = "username"
        password = "password"
        user = factories.User(username=username, password=password)

        # Set the http authorization header using basic auth
        credentials = f"{username}:{password}"
        http_authorization = "Basic " + base64.b64encode(
            credentials.encode(HTTP_HEADER_ENCODING)
        ).decode(HTTP_HEADER_ENCODING)
        auth_headers = {"HTTP_AUTHORIZATION": http_authorization}

        login_url = django_urls.reverse("login")
        response = rest_api_client.post(login_url, **auth_headers)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"expiry": None, "token": mock.ANY}

        assert user.auth_token_set.exists()

    def test_cannot_login_with_invalid_username_and_password(self, rest_api_client):
        # Try logging in with a non-existent username and password
        credentials = "username:password"
        http_authorization = "Basic " + base64.b64encode(
            credentials.encode(HTTP_HEADER_ENCODING)
        ).decode(HTTP_HEADER_ENCODING)
        auth_headers = {"HTTP_AUTHORIZATION": http_authorization}

        login_url = django_urls.reverse("login")
        response = rest_api_client.post(login_url, **auth_headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data == {
            "detail": drf_exceptions.ErrorDetail(
                string="Invalid username/password.", code="authentication_failed"
            )
        }

        assert not knox_models.AuthToken.objects.exists()

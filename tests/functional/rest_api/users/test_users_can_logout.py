# Third party imports
import pytest
from knox import models as knox_models
from rest_framework import status

# Django imports
from django import urls as django_urls

# Local application imports
from tests import factories


class TestLogout:
    def test_user_can_logout_and_this_deletes_token(self, rest_api_client):
        user = factories.User()
        token_instance, token = factories.AuthToken(user=user)

        # Set the http authorization header using token auth
        auth_headers = {"HTTP_AUTHORIZATION": f"Token {token}"}

        logout_url = django_urls.reverse("logout")
        response = rest_api_client.post(logout_url, **auth_headers)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Ensure the token has been deleted
        with pytest.raises(knox_models.AuthToken.DoesNotExist):
            token_instance.refresh_from_db()

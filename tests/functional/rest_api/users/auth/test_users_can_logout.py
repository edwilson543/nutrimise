# Third party imports
from rest_framework import status

# Django imports
from django import urls as django_urls

# Local application imports
from tests import factories


class TestLogout:
    def test_user_can_logout_and_this_deletes_token(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        assert user.auth_token_set.exists()

        logout_url = django_urls.reverse("logout")
        response = rest_api_client.post(logout_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Ensure the token has been deleted
        assert not user.auth_token_set.exists()

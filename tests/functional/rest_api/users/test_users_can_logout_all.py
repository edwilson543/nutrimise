# Third party imports
from rest_framework import status

# Django imports
from django import urls as django_urls

# Local application imports
from tests import factories


class TestLogoutAll:
    def test_logout_from_all_devices(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        # Create an extra auth token for the user, simulating login on some other device
        factories.AuthToken(user=user)

        assert user.auth_token_set.count() == 2

        logout_all_url = django_urls.reverse("logout-all")
        response = rest_api_client.post(logout_all_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not user.auth_token_set.exists()

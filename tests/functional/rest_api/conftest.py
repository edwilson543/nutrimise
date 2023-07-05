# Third party imports
import pytest
from knox import models as knox_models
from rest_framework import test as drf_test

# Django imports
from django.contrib.auth import models as auth_models

# Local application imports
from tests import factories


class APIClient(drf_test.APIClient):
    def authorize_user(self, user: auth_models.User) -> knox_models.AuthToken:
        """
        Generation an auth token and set it in the http authorization header.
        """
        token_instance, token = factories.AuthToken(user=user)
        auth_headers = {"HTTP_AUTHORIZATION": f"Token {token}"}
        super().credentials(**auth_headers)
        return token_instance


@pytest.fixture
def rest_api_client() -> APIClient:
    yield APIClient()


@pytest.fixture(autouse=True)
def auto_enable_db_access(db) -> None:
    yield

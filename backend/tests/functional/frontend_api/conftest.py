import pytest
from django.contrib.auth import models as auth_models
from fastapi import testclient

from nutrimise.interfaces.frontend_api import app, auth


class TestClient(testclient.TestClient):
    def set_authenticated_user(self, user: auth_models.User) -> None:
        # Mypy doesn't know about `dependency_overrides`.
        self.app.dependency_overrides[auth.get_authenticated_user] = lambda: user  # type: ignore[attr-defined]


@pytest.fixture
def frontend_api_client(db) -> TestClient:
    return TestClient(app=app.api)

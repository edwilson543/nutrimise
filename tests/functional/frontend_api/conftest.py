import pytest
from fastapi import testclient

from nutrimise.interfaces.frontend_api import app


@pytest.fixture(scope="session")
def frontend_api_client() -> testclient.TestClient:
    return testclient.TestClient(app=app.api)

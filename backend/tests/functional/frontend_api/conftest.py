import pytest
from fastapi import testclient

from nutrimise.interfaces.frontend_api import app


@pytest.fixture
def frontend_api_client(db) -> testclient.TestClient:
    return testclient.TestClient(app=app.api)

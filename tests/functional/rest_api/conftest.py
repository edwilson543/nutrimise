# Third party imports
import pytest
from rest_framework import test as drf_test


@pytest.fixture
def rest_api_client() -> drf_test.APIClient:
    yield drf_test.APIClient()


@pytest.fixture(autouse=True)
def auto_enable_db_access(db) -> None:
    yield

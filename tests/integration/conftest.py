# Standard library imports
from typing import Generator

# Third party imports
import pytest


@pytest.fixture(autouse=True)
def auto_enable_db_access_for_integration_tests(db) -> Generator[None, None, None]:
    yield

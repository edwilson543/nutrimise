from typing import Generator

import pytest


@pytest.fixture(autouse=True)
def grant_db_access_to_management_functional_tests(db) -> Generator[None, None, None]:
    yield

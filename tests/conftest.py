# Standard library imports
import shutil

# Third party imports
import pytest

# Django imports
from django.conf import settings
from django.test import override_settings

TEST_MEDIA_ROOT = settings.BASE_DIR / "tmp"


@pytest.fixture(autouse=True)
def use_temp_directory_as_media_root_for_tests() -> None:
    with override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT):
        yield


def pytest_sessionfinish(session, exitstatus) -> None:
    shutil.rmtree(TEST_MEDIA_ROOT)
    # super(session, exitstatus)

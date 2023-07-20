# Standard library imports
import pathlib
import shutil

# Third party imports
import pytest

# Django imports
from django.conf import settings
from django.test import override_settings

TEST_MEDIA_ROOT = settings.BASE_DIR / "tmp"


@pytest.fixture(autouse=True)
def use_temp_directory_as_media_root_for_tests() -> None:
    """
    Store media files in a temporary directory during tests.
    """
    with override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT):
        yield


def pytest_sessionfinish() -> None:
    """
    Delete the temporary media directory made during tests.
    """
    if pathlib.Path.is_dir(TEST_MEDIA_ROOT):
        shutil.rmtree(TEST_MEDIA_ROOT)

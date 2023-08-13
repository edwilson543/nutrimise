# Standard library imports
import pathlib
import shutil

# Third party imports
from plugins.storage import _local as local_storage

# Django imports
from django.conf import settings
from django.test import override_settings

# Local application imports
from tests import factories

TEST_MEDIA_ROOT = settings.BASE_DIR / "tmp"


class TestLocalFileStorage:
    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
    def test_uploads_file_to_filesystem(self):
        file = factories.image().file
        storage_context = local_storage.StorageContext(
            namespace=local_storage.Namespace.RECIPES, filename="test.jpeg"
        )

        store = local_storage.LocalFileStorage()

        store.upload(file=file, storage_context=storage_context)

        assert pathlib.Path.is_file(storage_context.filepath)

        self._remove_tmp_files(filepath=storage_context.filepath)

    def _remove_tmp_files(self, filepath: pathlib.Path):
        pathlib.Path.unlink(filepath)
        shutil.rmtree(TEST_MEDIA_ROOT)

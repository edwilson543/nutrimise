# Django imports
from django.test import override_settings

# Local application imports
from domain.storage import _config as storage_config
from tests.helpers import storage as storage_helpers


class TestGetFileStorage:
    @override_settings(FILE_STORAGE_CLASS="tests.helpers.storage.TestFileStorage")
    def test_get_file_storage(self):
        storage_class = storage_config.get_file_storage()

        assert isinstance(storage_class, storage_helpers.TestFileStorage)
        assert storage_class.context_class == storage_helpers.StorageContext

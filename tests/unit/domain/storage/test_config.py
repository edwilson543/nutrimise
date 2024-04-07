# Local application imports
from reciply.domain.storage import _config as storage_config
from tests.helpers import storage as storage_helpers


class TestGetFileStorage:
    @storage_helpers.install_test_file_storage
    def test_get_file_storage(self):
        storage_class = storage_config.get_file_storage()

        assert isinstance(storage_class, storage_helpers.TestFileStorage)
        assert storage_class.context_class == storage_helpers.StorageContext

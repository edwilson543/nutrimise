# Third party imports
import pytest

# Local application imports
from app.menus import _delete_menu_item
from data.menus import models as menu_models
from tests import factories


class TestRemoveItemFromMenu:
    def test_removes_menu_item(self):
        menu_item = factories.MenuItem()

        _delete_menu_item.delete_menu_item(item=menu_item)

        with pytest.raises(menu_models.MenuItem.DoesNotExist):
            menu_item.refresh_from_db()

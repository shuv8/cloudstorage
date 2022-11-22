import pytest

from base_storage_item import BaseStorageItem
from complaints_space import ComplaintsSpace


class TestComplaintsSpace:
    @pytest.fixture(scope='function')
    def complaints_space(self):
        return ComplaintsSpace()

    def test_decline_complain(self, complaints_space):
        assert complaints_space.decline_complain(BaseStorageItem()) is None

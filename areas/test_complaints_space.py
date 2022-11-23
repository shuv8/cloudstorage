import pytest

from base_storage_item import BaseStorageItem
from complaints_space import ComplaintsSpace, DirectoryManager


class TestComplaintsSpace:
    @pytest.fixture(scope='function')
    def complaints_space(self):
        return ComplaintsSpace()

    def test_decline_complain(self, complaints_space):
        assert complaints_space.decline_complain(BaseStorageItem()) is None

    def test_provide_main_directory(self, complaints_space):
        assert isinstance(complaints_space.provide_main_directory(), DirectoryManager)

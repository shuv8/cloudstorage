import pytest

from space_manager import SpaceManager, Directory
from files import File


class TestSpaceManager:
    @pytest.fixture(scope='function')
    def space_manager(self):
        return SpaceManager()

    def test_create_space_by_directory(self, space_manager):
        assert space_manager.create_space_by_directory(Directory()) is None
        try:
            space_manager.create_space_by_directory(123)
        except TypeError:
            pass

    def test_create_space_by_file(self, space_manager):
        assert space_manager.create_space_by_file(File()) is None
        try:
            space_manager.create_space_by_file(123)
        except TypeError:
            pass

    def test_remove_cloud_space(self, space_manager):
        assert space_manager.remove_cloud_space("ASDASD") is None

    def test_get_spaces(self, space_manager):
        assert space_manager.get_spaces() == []

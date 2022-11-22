import pytest

from directory_manager import DirectoryManager


class TestDirectoryManager:
    @pytest.fixture(scope='function')
    def directory_manager(self):
        return DirectoryManager()

    def test_create_dir(self, directory_manager):
        assert 1 == 1  # TODO

    def test_remove_dir(self, directory_manager):
        assert 1 == 1  # TODO

    def test_get_dir(self, directory_manager):
        assert 1 == 1  # TODO

    def test_set_items(self, directory_manager):
        assert 1 == 1  # TODO

    def test_get_items(self, directory_manager):
        assert 1 == 1  # TODO

    def test_set_directory_manager(self, directory_manager):
        assert 1 == 1  # TODO

    def test_get_directory_manager(self, directory_manager):
        assert 1 == 1  # TODO

    def test_set_file_manager(self, directory_manager):
        assert 1 == 1  # TODO

    def test_get_file_manager(self, directory_manager):
        assert 1 == 1  # TODO

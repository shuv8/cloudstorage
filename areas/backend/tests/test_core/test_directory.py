import pytest

from core.directory import Directory
from core.directory_manager import DirectoryManager


@pytest.fixture()
def directory():
    return Directory(
        name="test",
    )


@pytest.fixture()
def directory_manager():
    return DirectoryManager(
        items=None,
        file_manager=None
    )


class TestDirectory:

    def test_directory_manager_property(self, directory, directory_manager):
        directory.directory_manager = directory_manager
        assert directory.directory_manager == directory_manager

        with pytest.raises(TypeError):
            directory.directory_manager = 43

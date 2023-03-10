import pytest

from core.directory import Directory
from core.directory_manager import DirectoryManager
from core.files import FileManager, File


@pytest.fixture()
def directory_manager():
    return DirectoryManager(
        items=None,
        file_manager=None
    )


@pytest.fixture()
def file_manager():
    return FileManager(
        items=None,
    )



@pytest.fixture()
def directory():
    return Directory(
        name="test",
    )


class TestDirectoryManager:

    def test_create_dir(self, directory_manager):
        assert directory_manager.create_dir("asd") is None
        assert directory_manager.get_dir("asd").name == "asd"

        with pytest.raises(TypeError):
            directory_manager.create_dir(123)

    def test_remove_dir(self, directory_manager):
        directory_manager.create_dir("asd")
        assert directory_manager.remove_dir("asd") is None

        with pytest.raises(FileNotFoundError):
            directory_manager.get_dir("asd")

        with pytest.raises(TypeError):
            directory_manager.remove_dir(123)

    def test_get_dir(self, directory_manager):
        directory_manager.create_dir("asd")
        assert directory_manager.get_dir("asd").get_name() == "asd"

        with pytest.raises(TypeError):
            directory_manager.get_dir(123)

    def test_set_get_items(self, directory_manager, directory):
        directory_manager.items = [directory]
        assert directory_manager.items == [directory]

        with pytest.raises(TypeError):
            directory_manager.items = "trq"

    def test_add_items(self, directory_manager, directory):
        directory_manager.add_items([directory])
        assert directory_manager.items == [directory]

        with pytest.raises(TypeError):
            directory_manager.add_items(43)

        with pytest.raises(TypeError):
            directory_manager.add_items([43, directory])

    def test_set_get_file_manager(self, directory_manager, file_manager):
        directory_manager.file_manager = file_manager
        assert directory_manager.file_manager == file_manager

        with pytest.raises(TypeError):
            directory_manager.set_file_manager("trq")

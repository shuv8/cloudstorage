import pytest

from cloud_storage_service.files import File, FileManager


@pytest.fixture()
def file():
    return File(
        name="test",
        _type=".txt",
    )


@pytest.fixture()
def file2():
    return File(
        name="test2",
        _type=".txt2"
    )


@pytest.fixture()
def file_manager():
    return FileManager(
        items=None,
    )



class TestFileManager:
    def test_set_get_items(self, file_manager, file):
        file_manager.items = [file]
        assert file_manager.items == [file]

        with pytest.raises(TypeError):
            file_manager.items = "trq"

    def test_add_item(self, file_manager, file2):
        file_manager.add_item(file2)
        assert file_manager.items == [file2]

        with pytest.raises(TypeError):
            file_manager.add_item(34)

    def test_remove_item(self, file_manager, file2):
        file_manager.add_item(file2)
        assert file_manager.items == [file2]

        file_manager.remove_item(file2)
        assert file_manager.items == []

        with pytest.raises(TypeError):
            file_manager.remove_item(34)

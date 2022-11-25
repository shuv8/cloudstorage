import uuid

import pytest

from cloud_storage_service.directory import Directory
from cloud_storage_service.files import File
from cloud_storage_service.space_manager import SpaceManager


@pytest.fixture()
def space_manager():
    return SpaceManager(
        spaces=None
    )


@pytest.fixture()
def file():
    return File(
        name="test",
        _type=".txt",
    )


@pytest.fixture()
def directory():
    return Directory(
        name="test",
    )


class TestSpaceManager:

    def test_create_space_by_file(self, space_manager, file):
        assert len(space_manager.get_spaces()) == 1
        assert space_manager.create_space_by_file(file) is None

        assert len(space_manager.get_spaces()) == 2
        assert space_manager.get_spaces()[1].get_directory_manager().file_manager.items[0] == file

        with pytest.raises(TypeError):
            space_manager.create_space_by_file(42)

    def test_create_space_by_directory(self, space_manager, directory):
        assert len(space_manager.get_spaces()) == 1
        assert space_manager.create_space_by_directory(directory) is None

        assert len(space_manager.get_spaces()) == 2
        assert space_manager.get_spaces()[1].get_directory_manager().items[0] == directory

        with pytest.raises(TypeError):
            space_manager.create_space_by_directory(42)

    def test_remove_cloud_space(self, space_manager, directory):
        assert space_manager.create_space_by_directory(directory) is None
        assert len(space_manager.get_spaces()) == 2
        assert space_manager.remove_cloud_space(space_manager.get_spaces()[1].get_id()) is None
        assert len(space_manager.get_spaces()) == 1

        with pytest.raises(TypeError):
            space_manager.remove_cloud_space(42)

        with pytest.raises(ValueError):
            space_manager.remove_cloud_space(uuid.uuid4())

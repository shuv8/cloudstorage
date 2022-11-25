from __future__ import annotations
import uuid

import pytest

from cloud_storage_service.directory_manager import DirectoryManager
from cloud_storage_service.user_cloud_space import UserCloudSpace, SpaceType

_id = uuid.uuid4()


@pytest.fixture()
def directory_manager():
    return DirectoryManager(
        items=None,
        file_manager=None
    )


@pytest.fixture()
def user_cloud_space(directory_manager):
    return UserCloudSpace(
        _id=_id,
        space_type=SpaceType.Regular,
        directory_manager=directory_manager
    )


class TestUserCloudSpace:

    def test_get_id(self, user_cloud_space):
        assert user_cloud_space.get_id() == _id

    def test_get_space_type(self, user_cloud_space):
        assert user_cloud_space.get_space_type() == SpaceType.Regular

    def test_get_directory_manager(self, user_cloud_space, directory_manager):
        assert user_cloud_space.get_directory_manager() == directory_manager

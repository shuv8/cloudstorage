import pytest

from user_cloud_space import UserCloudSpace, DirectoryManager


class TestUserCloudSpace:
    @pytest.fixture(scope='function')
    def user_cloud_space(self):
        return UserCloudSpace()

    def test_provide_data(self, user_cloud_space):
        assert isinstance(user_cloud_space.provide_data(), UserCloudSpace)

    def test_provide_main_directory(self, user_cloud_space):
        assert isinstance(user_cloud_space.provide_main_directory(), DirectoryManager)

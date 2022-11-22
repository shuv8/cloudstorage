import pytest

from user_cloud_space import UserCloudSpace


class TestUserCloudSpace:
    @pytest.fixture(scope='function')
    def user_cloud_space(self):
        return UserCloudSpace()

    def test_provide_data(self, user_cloud_space):
        assert isinstance(user_cloud_space.provide_data(), UserCloudSpace)

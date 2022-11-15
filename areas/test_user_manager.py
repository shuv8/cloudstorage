import pytest

from user_manager import UserManager


class TestUserManager:
    @pytest.fixture(scope='function')
    def user_manager(self):
        return UserManager()

    def test_get_users(self, user_manager):
        assert 1 == 1  # TODO

    def test_set_users(self, user_manager):
        assert 1 == 1  # TODO

    def test_add_user(self, user_manager):
        assert 1 == 1  # TODO

    def test_get_user(self, user_manager):
        assert 1 == 1  # TODO

    def test_edit_user(self, user_manager):
        assert 1 == 1  # TODO

    def test_remove_user(self, user_manager):
        assert 1 == 1  # TODO

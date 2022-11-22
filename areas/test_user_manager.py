import pytest

from user import User
from user_manager import UserManager


class TestUserManager:
    @pytest.fixture(scope='function')
    def user_manager(self):
        return UserManager()

    def test_get_users(self, user_manager):
        assert user_manager.get_users() == []

    def test_set_users(self, user_manager):
        assert user_manager.set_users([]) is None
        try:
            user_manager.set_users("asd")
        except TypeError:
            pass

    def test_add_user(self, user_manager):
        assert user_manager.add_user(User()) is None
        try:
            user_manager.add_user("asd")
        except TypeError:
            pass

    def test_get_user(self, user_manager):
        user_to_add = User()
        user_to_add.set_email("qwe@qwe.qwe")
        um = user_manager
        um.add_user(user_to_add)
        assert type(um.get_user("qwe@qwe.qwe")) is User
        assert user_manager.get_user("asd@asd.asd") is None

    def test_edit_user(self, user_manager):
        assert user_manager.edit_user(User()) is None

    def test_remove_user(self, user_manager):
        user_to_add = User()
        um = user_manager
        um.add_user(user_to_add)
        assert um.remove_user(user_to_add) is None
        try:
            user_manager.remove_user("asd")
        except TypeError:
            pass

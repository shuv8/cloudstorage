import pytest

from department_manager import DepartmentManager
from space_manager import SpaceManager
from role import Role
from user import User


class TestUser:
    @pytest.fixture(scope='function')
    def user(self):
        return User()

    def test_get_email(self, user):
        user.set_email("asd@asd.asd")
        assert user.get_email() == "asd@asd.asd"

    def test_set_email(self, user):
        user.set_email("asd@asd.asd")
        assert user.get_email() == "asd@asd.asd"
        try:
            user.set_email(123)
        except TypeError:
            pass

    def test_get_password(self, user):
        user.set_password("pass123")
        assert user.get_password() == "pass123"

    def test_set_password(self, user):
        user.set_password("pass123")
        assert user.get_password() == "pass123"
        try:
            user.set_password(123)
        except TypeError:
            pass

    def test_get_username(self, user):
        user.set_username("user1")
        assert user.get_username() == "user1"

    def test_set_username(self, user):
        user.set_username("user1")
        assert user.get_username() == "user1"
        try:
            user.set_username(123)
        except TypeError:
            pass

    def test_get_role(self, user):
        assert user.get_role() is None

    def test_set_role(self, user):
        assert user.set_role(Role.ADMIN) is None
        try:
            user.set_role(123)
        except TypeError:
            pass

    def test_get_space_manager(self, user):
        assert user.get_space_manager() is None

    def test_set_space_manager(self, user):
        assert user.set_space_manager(SpaceManager()) is None
        try:
            user.set_space_manager(123)
        except TypeError:
            pass

    def test_get_department_manager(self, user):
        assert user.get_department_manager() is None

    def test_set_department_manager(self, user):
        assert user.set_department_manager(DepartmentManager()) is None
        try:
            user.set_department_manager(123)
        except TypeError:
            pass

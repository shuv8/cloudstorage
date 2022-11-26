import pytest

from cloud_storage_service.department_manager import DepartmentManager
from cloud_storage_service.role import Role
from cloud_storage_service.space_manager import SpaceManager
from cloud_storage_service.user import User
from cloud_storage_service.user_cloud_space import SpaceType


@pytest.fixture()
def user():
    return User(
        email="test_mail@mail.com",
        password="password",
        username="username",
    )


@pytest.fixture(scope='function')
def department_manager():
    return DepartmentManager(
        departments=None
    )


@pytest.fixture()
def space_manager():
    return SpaceManager(
        spaces=None
    )


class TestUser:

    def test_get_email(self, user):
        user.email = "asd@asd.asd"
        assert user.email == "asd@asd.asd"

    def test_set_email(self, user):
        user.email = "asd@asd.asd"
        assert user.email == "asd@asd.asd"
        try:
            user.email = 123
        except TypeError:
            pass

    def test_get_password(self, user):
        user.password = "pass123"
        assert user.get_password() == "pass123"

    def test_set_password(self, user):
        user.password = "pass123"
        assert user.password == "pass123"
        try:
            user.password = 123
        except TypeError:
            pass

    def test_get_username(self, user):
        user.username = "user1"
        assert user.username == "user1"

    def test_set_username(self, user):
        user.username = "user1"
        assert user.username == "user1"
        try:
            user.username = 123
        except TypeError:
            pass

    def test_get_role(self, user):
        assert user.role == Role.Client

    def test_set_role(self, user):
        user.role = Role.Admin
        assert user.role == Role.Admin

        try:
            user.role = 123
        except TypeError:
            pass

    def test_get_default_space_manager(self, user):
        assert user.space_manager.get_spaces()[0].get_space_type() == SpaceType.Regular

    def test_set_space_manager(self, user, space_manager):
        user.space_manager = space_manager
        assert user.space_manager == space_manager
        try:
            user.space_manager = 123
        except TypeError:
            pass

    def test_get_department_manager(self, user):
        assert user.get_department_manager() is None

    def test_set_department_manager(self, user, department_manager):
        user.department_manager = department_manager
        assert user.department_manager == department_manager
        try:
            user.department_manager = 123
        except TypeError:
            pass

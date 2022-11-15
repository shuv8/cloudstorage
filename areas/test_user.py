import pytest

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

    def test_get_password(self, user):
        user.set_password("pass123")
        assert user.get_password() == "pass123"

    def test_set_password(self, user):
        user.set_password("pass123")
        assert user.get_password() == "pass123"

    def test_get_username(self, user):
        user.set_username("user1")
        assert user.get_username() == "user1"

    def test_set_username(self, user):
        user.set_username("user1")
        assert user.get_username() == "user1"

    def test_get_role(self, user):
        assert 1 == 1  # TODO

    def test_set_role(self, user):
        assert 1 == 1  # TODO

    def test_get_space_manager(self, user):
        assert 1 == 1  # TODO

    def test_set_space_manager(self, user):
        assert 1 == 1  # TODO

    def test_get_department_manager(self, user):
        assert 1 == 1  # TODO

    def test_set_department_manager(self, user):
        assert 1 == 1  # TODO

import pytest

from department import Department


class TestDepartment:
    @pytest.fixture(scope='function')
    def department(self):
        return Department()

    def test_get_department_name(self, department):
        department.set_department_name("company1")
        assert department.get_department_name() == "company1"

    def test_set_department_name(self, department):
        department.set_department_name("company1")
        assert department.get_department_name() == "company1"
        try:
            department.set_department_name(123)
        except TypeError:
            pass

    def test_get_users(self, department):
        assert department.get_users() == []

    def test_set_users(self, department):
        department.set_users([])
        assert department.get_users() == []
        try:
            department.set_users(123)
        except TypeError:
            pass
        try:
            department.set_users([123])
        except TypeError:
            pass

    def test_add_user(self, department):
        department.add_user("asd@asd.asd")
        assert department.get_users() == ["asd@asd.asd"]
        try:
            department.add_user(123)
        except TypeError:
            pass

    def test_remove_user(self, department):
        department.add_user("asd@asd.asd")
        assert department.remove_user("asd@asd.asd") is None
        try:
            department.remove_user(123)
        except TypeError:
            pass

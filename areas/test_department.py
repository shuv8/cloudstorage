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

    def test_get_users(self, department):
        assert 1 == 1  # TODO

    def test_set_users(self, department):
        assert 1 == 1  # TODO

    def test_add_user(self, department):
        assert 1 == 1  # TODO

    def test_remove_user(self, department):
        assert 1 == 1  # TODO

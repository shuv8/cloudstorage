import pytest

from department_manager import DepartmentManager


class TestDepartmentManager:
    @pytest.fixture(scope='function')
    def department_manager(self):
        return DepartmentManager()

    def test_add_department(self, department_manager):
        assert 1 == 1  # TODO

    def test_get_department(self, department_manager):
        assert 1 == 1  # TODO

    def test_remove_department_by_department_name(self, department_manager):
        assert 1 == 1  # TODO

    def test_add_user(self, department_manager):
        assert 1 == 1  # TODO

    def test_remove_user(self, department_manager):
        assert 1 == 1  # TODO

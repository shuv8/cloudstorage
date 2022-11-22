import pytest

from department import Department
from department_manager import DepartmentManager


class TestDepartmentManager:
    @pytest.fixture(scope='function')
    def department_manager(self):
        return DepartmentManager()

    def test_add_department(self, department_manager):
        assert department_manager.add_department(Department()) is None
        try:
            department_manager.add_department(123)
        except TypeError:
            pass

    def test_get_department(self, department_manager):
        department_to_add = Department()
        department_to_add.set_department_name("asd")
        department_manager.add_department(department_to_add)
        assert department_manager.get_department("asd") is not None
        assert department_manager.get_department("asd123") is None
        try:
            department_manager.get_department(123)
        except TypeError:
            pass

    def test_remove_department_by_department_name(self, department_manager):
        department_to_add = Department()
        department_to_add.set_department_name("asd")
        department_manager.add_department(department_to_add)
        assert department_manager.remove_department_by_department_name("asd") is None
        try:
            department_manager.remove_department_by_department_name(123)
        except TypeError:
            pass

    def test_add_user(self, department_manager):
        department_to_add = Department()
        department_to_add.set_department_name("asd")
        department_manager.add_department(department_to_add)
        assert department_manager.add_user("asd@asd.asd", "asd") is None

    def test_remove_user(self, department_manager):
        department_to_add = Department()
        department_to_add.set_department_name("asd")
        department_manager.add_department(department_to_add)
        department_manager.add_user("asd@asd.asd", "asd")
        assert department_manager.remove_user("asd@asd.asd", "asd") is None

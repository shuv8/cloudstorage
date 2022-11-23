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
        try:
            department_manager.add_user(123, "abc")
        except TypeError:
            pass
        try:
            department_manager.add_user("abc", 123)
        except TypeError:
            pass

    def test_remove_user(self, department_manager):
        department_to_add = Department()
        department_to_add.set_department_name("asd")
        department_manager.add_department(department_to_add)
        department_manager.add_user("asd@asd.asd", "asd")
        assert department_manager.remove_user("asd@asd.asd", "asd") is None
        assert department_manager.get_users_list_by_department_name("asd") == []
        try:
            department_manager.remove_user(123, "abc")
        except TypeError:
            pass
        try:
            department_manager.remove_user("abc", 123)
        except TypeError:
            pass

    def test_add_users_to_department(self, department_manager):
        department_to_add = Department()
        department_to_add.set_department_name("asd")
        department_manager.add_department(department_to_add)
        assert department_manager.add_users_to_department(["asd@asd.asd", "qwe@qwe.qwe"], "asd") is None
        assert department_manager.get_users_list_by_department_name("asd") == ["asd@asd.asd", "qwe@qwe.qwe"]
        try:
            department_manager.add_users_to_department(123, "abc")
        except TypeError:
            pass
        try:
            department_manager.add_users_to_department(["abc"], 123)
        except TypeError:
            pass

    def test_remove_users(self, department_manager):
        department_to_add = Department()
        department_to_add.set_department_name("asd")
        department_manager.add_department(department_to_add)
        department_manager.add_user("asd@asd.asd", "asd")
        department_manager.add_user("qwe@qwe.qwe", "asd")
        assert department_manager.remove_users(["asd@asd.asd", "qwe@qwe.qwe"], "asd") is None
        assert department_manager.get_users_list_by_department_name("asd") == []
        try:
            department_manager.remove_users(123, "abc")
        except TypeError:
            pass
        try:
            department_manager.remove_users(["abc"], 123)
        except TypeError:
            pass

    def test_add_users_to_departments(self, department_manager):
        department_to_add1 = Department()
        department_to_add1.set_department_name("asd")
        department_manager.add_department(department_to_add1)
        department_to_add2 = Department()
        department_to_add2.set_department_name("bcd")
        department_manager.add_department(department_to_add2)
        assert department_manager.add_users_to_departments(["asd@asd.asd", "qwe@qwe.qwe"], ["asd", "bcd"]) is None
        assert department_manager.get_users_list_by_department_name("asd") == ["asd@asd.asd", "qwe@qwe.qwe"]
        assert department_manager.get_users_list_by_department_name("bcd") == ["asd@asd.asd", "qwe@qwe.qwe"]
        try:
            department_manager.add_users_to_departments(123, ["abc"])
        except TypeError:
            pass
        try:
            department_manager.add_users_to_departments(["abc"], 123)
        except TypeError:
            pass

    def test_get_department_by_user_email(self, department_manager):
        assert department_manager.get_department_by_user_email("asd@asd.asd") is None
        department_to_add = Department()
        department_to_add.set_department_name("dep")
        department_to_add.add_user("asd@asd.asd")
        department_manager.add_department(department_to_add)
        assert department_manager.get_department_by_user_email("asd@asd.asd").get_department_name() == "dep"
        try:
            department_manager.get_department_by_user_email(123)
        except TypeError:
            pass

    def test_get_users_list_by_department_name(self, department_manager):
        assert department_manager.get_users_list_by_department_name("depDoesntExist") is None
        department_to_add = Department()
        department_to_add.set_department_name("dep")
        department_to_add.add_user("asd@asd.asd")
        department_manager.add_department(department_to_add)
        assert department_manager.get_users_list_by_department_name("dep") == ["asd@asd.asd"]
        try:
            department_manager.get_users_list_by_department_name(123)
        except TypeError:
            pass

from department import Department
from user import User


class DepartmentManager:
    __departments: list = None

    def __init__(self):
        self.__departments = []

    def add_department(self, new_department: Department):
        if isinstance(new_department, Department):
            self.__departments.append(new_department)
        else:
            raise TypeError

    def get_department(self, department_name: str) -> Department:
        for i in range(len(self.__departments)):
            if self.__departments[i].get_department_name() == department_name:
                return self.__departments[i]
        pass

    def remove_department_by_department_name(self, department_name: str):
        for i in range(len(self.__departments)):
            if self.__departments[i].get_department_name() == department_name:
                self.__departments.pop(i)

    def add_user(self, user: User, department_name: str):
        for i in range(len(self.__departments)):
            if self.__departments[i].get_department_name() == department_name:
                self.__departments[i].addUser(user)

    def remove_user(self, user: User, department_name: str):
        for i in range(len(self.__departments)):
            if self.__departments[i].get_department_name() == department_name:
                self.__departments[i].remove(user)

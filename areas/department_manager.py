from department import Department


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
        if isinstance(department_name, str):
            for i in range(len(self.__departments)):
                if self.__departments[i].get_department_name() == department_name:
                    return self.__departments[i]
            pass
        else:
            raise TypeError

    def remove_department_by_department_name(self, department_name: str):
        if isinstance(department_name, str):
            for i in range(len(self.__departments)):
                if self.__departments[i].get_department_name() == department_name:
                    self.__departments.pop(i)
        else:
            raise TypeError

    def add_user(self, user: str, department_name: str):
        for i in range(len(self.__departments)):
            if self.__departments[i].get_department_name() == department_name:
                self.__departments[i].add_user(user)

    def remove_user(self, user: str, department_name: str):
        for i in range(len(self.__departments)):
            if self.__departments[i].get_department_name() == department_name:
                self.__departments[i].remove_user(user)

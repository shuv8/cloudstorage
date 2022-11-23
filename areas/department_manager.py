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

    def add_user(self, user_email: str, department_name: str):
        if isinstance(user_email, str) and isinstance(department_name, str):
            for i in range(len(self.__departments)):
                if self.__departments[i].get_department_name() == department_name:
                    self.__departments[i].add_user(user_email)
        else:
            raise TypeError

    def remove_user(self, user_email: str, department_name: str):
        if isinstance(user_email, str) and isinstance(department_name, str):
            for i in range(len(self.__departments)):
                if self.__departments[i].get_department_name() == department_name:
                    self.__departments[i].remove_user(user_email)
        else:
            raise TypeError

    def add_users_to_department(self, users_emails: list, department_name: str):
        if isinstance(users_emails, list) and isinstance(department_name, str):
            for i in range(len(self.__departments)):
                if self.__departments[i].get_department_name() == department_name:
                    for j in range(len(users_emails)):
                        self.__departments[i].add_user(users_emails[j])
        else:
            raise TypeError

    def remove_users(self, users_emails: list, department_name: str):
        if isinstance(users_emails, list) and isinstance(department_name, str):
            for i in range(len(self.__departments)):
                if self.__departments[i].get_department_name() == department_name:
                    for j in range(len(users_emails)):
                        self.__departments[i].remove_user(users_emails[j])
        else:
            raise TypeError

    def add_users_to_departments(self, users_emails: list, departments_names: list):
        if isinstance(users_emails, list) and isinstance(departments_names, list):
            for i in range(len(self.__departments)):
                for j in range(len(departments_names)):
                    if self.__departments[i].get_department_name() == departments_names[j]:
                        self.add_users_to_department(users_emails, departments_names[j])
        else:
            raise TypeError

    def get_department_by_user_email(self, email: str) -> Department:
        if isinstance(email, str):
            for i in range(len(self.__departments)):
                lst = self.__departments[i].get_users()
                for j in range(len(lst)):
                    if lst[j] == email:
                        return self.__departments[i]
            pass
        else:
            raise TypeError

    def get_users_list_by_department_name(self, department_name: str) -> list:
        if isinstance(department_name, str):
            for i in range(len(self.__departments)):
                if self.__departments[i].get_department_name() == department_name:
                    return self.__departments[i].get_users()
            pass
        else:
            raise TypeError

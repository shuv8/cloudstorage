from enum import Enum


class Access(Enum):
    View = 1
    Edit = 2


class AccessType(Enum):
    Url = 1
    User = 2
    Department = 3


class BaseAccess:
    def __init__(self, access_type: Access = Access.View) -> None:
        self.__access_type = access_type

    def get_access_type(self) -> Access:
        return self.__access_type

    def set_access_type(self, new_type: Access = Access.View) -> None:
        if isinstance(new_type, Access):
            self.__access_type = new_type
        else:
            raise TypeError

    access_type = property(get_access_type, set_access_type)


class UrlAccess(BaseAccess):
    def __init__(self, url: str, access_type: Access = Access.View):
        super().__init__(access_type)
        self.__url = url

    def get_url(self):
        return self.__url


class UserAccess(BaseAccess):
    def __init__(self, email: str, access_type: Access = Access.View):
        super().__init__(access_type)
        self.__email = email

    def get_email(self):
        return self.__email


class DepartmentAccess(BaseAccess):
    def __init__(self, department_name: str, access_type: Access = Access.View):
        super().__init__(access_type)
        self.__department_name = department_name

    def get_department_name(self):
        return self.__department_name

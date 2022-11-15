from department_manager import DepartmentManager
from role import Role


class User:
    __email: str = None
    __password: str = None
    __username: str = None
    __role: Role = None
    __space_manager: SpaceManager = None
    __department_manager: DepartmentManager = None

    def get_email(self) -> str:
        return self.__email

    def set_email(self, new_email: str):
        if isinstance(new_email, str):
            self.__email = new_email
        else:
            raise TypeError

    def get_password(self) -> str:
        return self.__password

    def set_password(self, new_password: str):
        if isinstance(new_password, str):
            self.__password = new_password
        else:
            raise TypeError

    def get_username(self) -> str:
        return self.__password

    def set_username(self, new_username: str):
        if isinstance(new_username, str):
            self.__username = new_username
        else:
            raise TypeError

    def get_role(self) -> Role:
        return self.__role

    def set_role(self, new_role: Role):
        if isinstance(new_role, Role):
            self.__role = new_role
        else:
            raise TypeError

    def get_space_manager(self) -> SpaceManager:
        return self.__space_manager

    def set_space_manager(self, new_space_manager: SpaceManager):
        if isinstance(new_space_manager, SpaceManager):
            self.__space_manager = new_space_manager
        else:
            raise TypeError

    def get_department_manager(self) -> DepartmentManager:
        return self.__department_manager

    def set_department_manager(self, new_department_manager: DepartmentManager):
        if isinstance(new_department_manager, DepartmentManager):
            self.__department_manager = new_department_manager
        else:
            raise TypeError

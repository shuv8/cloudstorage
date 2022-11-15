from user import User


class Department:
    __department_name: str = None
    __users: list = None

    def get_department_name(self) -> str:
        return self.__department_name

    def set_department_name(self, new_department_name: str):
        if isinstance(new_department_name, str):
            self.__department_name = new_department_name
        else:
            raise TypeError

    def get_users(self) -> list:
        return self.__users

    def set_users(self, new_users: list):
        if all(map(lambda new_user: isinstance(new_user, User), new_users)):
            self.__users = new_users
        else:
            raise TypeError

    def add_user(self, new_user: User):
        if isinstance(new_user, User):
            self.__users.append(new_user)
        else:
            raise TypeError

    def remove_user(self, user: User):
        if isinstance(user, User):
            self.__users.remove(user)
        else:
            raise TypeError

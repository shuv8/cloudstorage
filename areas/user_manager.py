from user import User


class UserManager:
    __users: list = None

    def __init__(self):
        self.__users = []

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

    def get_user(self, email: str) -> User:
        for i in range(len(self.__users)):
            if self.__users[i].get_email() == email:
                return self.__users[i]
        pass

    def edit_user(self, user: User) -> User:
        pass  # TODO

    def remove_user(self, user: User):
        if isinstance(user, User):
            self.__users.remove(user)
        else:
            raise TypeError

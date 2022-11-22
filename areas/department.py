class Department:
    __department_name: str = None
    __users_emails: list = None

    def __init__(self):
        self.__users_emails = []

    def get_department_name(self) -> str:
        return self.__department_name

    def set_department_name(self, new_department_name: str):
        if isinstance(new_department_name, str):
            self.__department_name = new_department_name
        else:
            raise TypeError

    def get_users(self) -> list:
        return self.__users_emails

    def set_users(self, new_users_emails: list):
        if isinstance(new_users_emails, list):
            if all(map(lambda new_user: isinstance(new_user, str), new_users_emails)):
                self.__users_emails = new_users_emails
            else:
                raise TypeError
        else:
            raise TypeError

    def add_user(self, email: str):
        if isinstance(email, str):
            self.__users_emails.append(email)
        else:
            raise TypeError

    def remove_user(self, email: str):
        if isinstance(email, str):
            self.__users_emails.remove(email)
        else:
            raise TypeError

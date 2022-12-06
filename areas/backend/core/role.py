from enum import Enum


class Role(Enum):
    Admin = 1
    Client = 2

    @staticmethod
    def get_enum_from_value(value):
        if str(value) == "1":
            return Role.Admin
        if str(value) == "2":
            return Role.Client
        else:
            raise NotImplementedError

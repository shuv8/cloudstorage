import uuid

from accesses import BaseAccess


class BaseStorageItem:
    __id: uuid.UUID = None
    __name: str = None
    __accesses: list = None

    def get_id(self) -> uuid.UUID:
        return self.__id

    def set_id(self, new_id: uuid.UUID):
        if isinstance(new_id, uuid.UUID):
            self.__id = new_id
        else:
            raise TypeError

    def get_name(self) -> str:
        return self.__name

    def set_name(self, new_name: str):
        if isinstance(new_name, str):
            self.__name = new_name
        else:
            raise TypeError

    def get_accesses(self) -> list:
        return self.__accesses

    def set_accesses(self, new_accesses: list):
        if all(map(lambda new_access: isinstance(new_access, BaseAccess), new_accesses)):
            self.__accesses = new_accesses
        else:
            raise TypeError

    def add_access(self, new_access: BaseAccess):
        if isinstance(new_access, BaseAccess):
            self.__accesses.append(new_access)
        else:
            raise TypeError

    def remove_access(self, access: BaseAccess):
        if isinstance(access, BaseAccess):
            self.__accesses.remove(access)
        else:
            raise TypeError

import uuid
from typing import Optional

from core.accesses import BaseAccess


class BaseStorageItem:

    def __init__(
            self,
            name: str,
            accesses: Optional[list[BaseAccess]],
            _id=uuid.uuid4()
    ):
        self.__id = _id
        self.__name: str = name
        self.__is_suspicious = False
        self.__accesses: list[BaseAccess] = accesses or list()

    def get_id(self) -> uuid.UUID:
        return self.__id

    def set_id(self, new_id: uuid.UUID):
        if isinstance(new_id, uuid.UUID):
            self.__id = new_id
        else:
            raise TypeError

    id = property(get_id, set_id)

    def get_name(self) -> str:
        return self.__name

    def set_name(self, new_name: str):
        if isinstance(new_name, str):
            self.__name = new_name
        else:
            raise TypeError

    name = property(get_name, set_name)

    def get_suspicious(self) -> bool:
        return self.__is_suspicious

    def set_suspicious(self, is_suspicious: bool):
        if isinstance(is_suspicious, bool):
            self.__is_suspicious = is_suspicious
        else:
            raise TypeError

    is_suspicious = property(get_suspicious, set_suspicious)

    def get_accesses(self) -> list[BaseAccess]:
        return self.__accesses

    def set_accesses(self, new_accesses: list[BaseAccess]):
        if all(map(lambda new_access: isinstance(new_access, BaseAccess), new_accesses)):
            self.__accesses = new_accesses
        else:
            raise TypeError

    accesses = property(get_accesses, set_accesses)

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

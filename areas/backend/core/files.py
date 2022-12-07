import uuid
from typing import Optional

from core.accesses import BaseAccess
from core.base_storage_item import BaseStorageItem


class File(BaseStorageItem):
    def __init__(
            self,
            name: str,
            _type: str,
            _id: Optional[uuid.UUID] = None,
            accesses: Optional[list[BaseAccess]] = None,
    ):
        _id = _id or uuid.uuid4()
        super().__init__(name, accesses, _id)
        self.__type = _type

    def get_type(self) -> str:
        return self.__type

    def set_type(self, new_type: str):
        if isinstance(new_type, str):
            self.__type = new_type
        else:
            raise TypeError

    type = property(get_type, set_type)


class FileManager:
    def __init__(self, items: Optional[list[File]]):
        self.__items = items or list()

    def get_items(self) -> list[File]:
        return self.__items

    def set_items(self, new_items: list[File]):
        if all(map(lambda new_item: isinstance(new_item, File), new_items)):
            self.__items = new_items
        else:
            raise TypeError

    items = property(get_items, set_items)

    def add_item(self, new_item: File):
        if isinstance(new_item, File):
            self.__items.append(new_item)
        else:
            raise TypeError

    def remove_item(self, item: File):
        if isinstance(item, File):
            self.__items.remove(item)
        else:
            raise TypeError

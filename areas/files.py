from base_storage_item import BaseStorageItem
from base_storage_manager import BaseStorageManager


class File(BaseStorageItem):
    __type: str = None

    def get_type(self) -> str:
        return self.__type

    def set_type(self, new_type: str):
        if isinstance(new_type, str):
            self.__type = new_type
        else:
            raise TypeError


class FileManager(BaseStorageManager):
    __items: list = None

    def get_items(self) -> list:
        return self.__items

    def set_items(self, new_items: list):
        if all(map(lambda new_item: isinstance(new_item, File), new_items)):
            self.__items = new_items
        else:
            raise TypeError

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

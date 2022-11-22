from base_storage_item import BaseStorageItem


class BaseStorageManager:
    __items: list = None

    def get_items(self) -> list:
        return self.__items

    def set_items(self, new_items: list):
        if all(map(lambda new_item: isinstance(new_item, BaseStorageItem), new_items)):
            self.__items = new_items
        else:
            raise TypeError

    def add_item(self, new_item: BaseStorageItem):
        if isinstance(new_item, BaseStorageItem):
            self.__items.append(new_item)
        else:
            raise TypeError

    def remove_item(self, item: BaseStorageItem):
        if isinstance(item, BaseStorageItem):
            self.__items.remove(item)
        else:
            raise TypeError

from __future__ import annotations

from typing import Optional

from core.files import FileManager

from core import directory


class DirectoryManager:

    def __init__(
            self,
            items: Optional[list[directory.Directory]],
            file_manager: Optional[FileManager]
    ):
        self.__items = items or list()
        self.__file_manager: FileManager = file_manager or FileManager(items=None)

    def create_dir(self, directory_name: str):
        if isinstance(directory_name, str):
            dir_to_add = directory.Directory(
                name=directory_name
            )
            self.__items.append(dir_to_add)
        else:
            raise TypeError

    def remove_dir(self, directory_name: str):
        if isinstance(directory_name, str):
            for item in self.__items:
                if item.name == directory_name:
                    self.__items.remove(item)
        else:
            raise TypeError

    def get_dir(self, directory_name: str) -> Optional[directory.Directory]:
        if isinstance(directory_name, str):
            for item in self.__items:
                if isinstance(item, directory.Directory):
                    if item.name == directory_name:
                        return item
            raise FileNotFoundError
        else:
            raise TypeError

    def set_items(self, items: list[directory.Directory]):
        if all(map(lambda item: isinstance(item, directory.Directory), items)):
            self.__items = items
        else:
            raise TypeError

    def add_items(self, items: list[directory.Directory]):
        for item in items:
            if isinstance(item, directory.Directory):
                self.__items.append(item)
            else:
                raise TypeError

    def get_items(self) -> list[directory.Directory]:
        return self.__items

    items = property(get_items, set_items)

    def set_file_manager(self, new_file_manager: FileManager):
        if isinstance(new_file_manager, FileManager):
            self.__file_manager = new_file_manager
        else:
            raise TypeError

    def get_file_manager(self) -> Optional[FileManager]:
        return self.__file_manager

    file_manager = property(get_file_manager, set_file_manager)

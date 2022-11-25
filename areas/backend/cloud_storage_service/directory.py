from __future__ import annotations
from typing import Optional

from cloud_storage_service.accesses import BaseAccess
from cloud_storage_service.base_storage_item import BaseStorageItem

from cloud_storage_service import directory_manager


class Directory(BaseStorageItem):
    def __init__(
            self,
            name: str,
            accesses: Optional[list[BaseAccess]] = None,
    ):
        super().__init__(name, accesses)

        self.__directory_manager = directory_manager.DirectoryManager(
            items=None,
            file_manager=None
        )

    def set_directory_manager(self, new_directory_manager: directory_manager.DirectoryManager):
        if isinstance(new_directory_manager, directory_manager.DirectoryManager):
            self.__directory_manager = new_directory_manager
        else:
            raise TypeError

    def get_directory_manager(self) -> Optional[directory_manager.DirectoryManager]:
        return self.__directory_manager

    directory_manager = property(get_directory_manager, set_directory_manager)

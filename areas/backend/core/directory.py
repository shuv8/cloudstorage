from __future__ import annotations

import uuid
from typing import Optional

from core.accesses import BaseAccess
from core.base_storage_item import BaseStorageItem

from core import directory_manager


class Directory(BaseStorageItem):
    def __init__(
            self,
            name: str,
            accesses: Optional[list[BaseAccess]] = None,
            _id: Optional[uuid.UUID] = None,
    ):
        super().__init__(name, accesses, _id)

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

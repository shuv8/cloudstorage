from abc import ABC

from abstract_space import AbstractSpace
from base_storage_item import BaseStorageItem


class DirectoryManager:
    ...


class ComplaintsSpace(AbstractSpace, ABC):

    def decline_complain(self, item: BaseStorageItem):
        pass

    def provide_main_directory(self) -> DirectoryManager:
        return DirectoryManager()

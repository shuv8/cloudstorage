import uuid
from abc import ABC

from areas.abstract_space import AbstractSpace


class DirectoryManager:
    ...


class UserCloudSpace(AbstractSpace, ABC):
    __space_id: uuid = None

    def provide_data(self):
        return self

    def provide_main_directory(self) -> DirectoryManager:
        return DirectoryManager()

# from directory_manager import DirectoryManager
from abc import ABC, abstractmethod


class DirectoryManager:
    ...


class AbstractSpace(ABC):

    @abstractmethod
    def provide_main_directory(self) -> DirectoryManager:
        ...

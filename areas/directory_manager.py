from base_storage_manager import BaseStorageManager
from abstract_space import AbstractSpace
from directory_manager import DirectoryManager
from file_manager import FileManager

class DirectoryManager:
    __items: list = None
    __directoryManager: DirectoryManager = None
    __fileManager: FileManager = None
    #TO DO

    def __init__(self):
        self.__items = []

    def __directoryManager__(self)
        self.__directoryManager #TO DO

    def __fileManager__(self)
        self.__fileManager #TO DO

    def create_dir(self, directory_name: str):
        if isinstance(directory_name, str):
            self.__directory.append(directory_name)
        else:
            raise TypeError

    def remove_dir(self, directory_name: str):
        if isinstance(directory_name, str):
            self.__directory.append(directory_name)
        else:
            raise TypeError

    def get_dir(self, directory_name: str) -> Directory:
        for i in range(len(self.__items)):
            if self.__items[i].get_directory_name() == directory_name:
                return self.__items[i]
        pass

    def set_items(self, directory_name: str):
        for i in range(len(self.__items)):
            if self.__items[i].get_directory_name() == directory_name:
                self.__items.pop(i)

    def get_items(self, directory_name: str):
        for i in range(len(self.__items)):
            if self.__items[i].get_directory_name() == directory_name:
                self.__items.pop(i)

    def set_directory_manager(self, new_directory_manager: DirectoryManager):
        if isinstance(new_directory_manager, DirectoryManager):
            self.__directory_manager = new_directory_manager
        else:
            raise TypeError

    def get_directory_manager(self) -> DirectoryManager:
        return self.__directory_manager

    def set_file_manager(self, new_file_manager: FileManager):
        if isinstance(new_file_manager, FileManager):
            self.__directory_manager = new_file_manager
        else:
            raise TypeError

    def get_file_manager(self) -> FileManager:
        return self.__directory_manager
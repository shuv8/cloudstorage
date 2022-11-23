from files import File
from directory import Directory
from files import FileManager


class DirectoryManager:
    __items: list = None
    __file_manager: FileManager = None

    def __init__(self):
        self.__items = []

    def create_dir(self, directory_name: str):
        if isinstance(directory_name, str):
            dir_to_add = Directory()
            dir_to_add.set_name(directory_name)
            self.__items.append(dir_to_add)
        else:
            raise TypeError

    def remove_dir(self, directory_name: str):
        if isinstance(directory_name, str):
            for i in range(len(self.__items)):
                if self.__items[i].get_name() == directory_name:
                    self.__items.pop(i)
        else:
            raise TypeError

    def get_dir(self, directory_name: str) -> Directory:
        if isinstance(directory_name, str):
            for i in range(len(self.__items)):
                if self.__items[i].get_name() == directory_name:
                    return self.__items[i]
            pass
        else:
            raise TypeError

    # def set_items(self, items: list):
    #     for item in items:
    #         if isinstance(item, Directory) or isinstance(item, File):
    #             self.__items.append(item)
    #     else:
    #         raise TypeError

    def get_items(self) -> list:
        return self.__items

    def set_file_manager(self, new_file_manager: FileManager):
        if isinstance(new_file_manager, FileManager):
            self.__file_manager = new_file_manager
        else:
            raise TypeError

    def get_file_manager(self) -> FileManager:
        return self.__file_manager

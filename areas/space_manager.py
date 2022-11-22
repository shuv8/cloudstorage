import uuid
from files import File


class Directory:
    ...


class SpaceManager:
    __spaces: list = None

    def __init__(self):
        self.__spaces = []

    def create_space_by_directory(self, directory: Directory):
        if isinstance(directory, Directory):
            self.__spaces.append(directory)
        else:
            raise TypeError

    def create_space_by_file(self, file: File):
        if isinstance(file, File):
            self.__spaces.append(file)
        else:
            raise TypeError

    def remove_cloud_space(self, space_id: uuid):
        pass

    def get_spaces(self) -> list:
        return self.__spaces

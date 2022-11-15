import uuid


class Directory:
    ...

from files import File


class SpaceManager:
    __spaces: list = None

    def create_space_by_directory(self, directory: Directory):
        self.__spaces.append(directory)

    def create_space_by_file(self, file: File):
        self.__spaces.append(file)

    def remove_cloud_space(self, space_id: uuid):
        pass

    def get_spaces(self) -> list:
        pass

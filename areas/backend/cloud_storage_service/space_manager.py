import uuid
from typing import Optional

from cloud_storage_service.directory import Directory
from cloud_storage_service.directory_manager import DirectoryManager
from cloud_storage_service.files import File, FileManager
from cloud_storage_service.user_cloud_space import UserCloudSpace, SpaceType


class SpaceManager:
    def __init__(self, spaces: Optional[list[UserCloudSpace]]):
        self.__spaces = spaces or [self.__create_default_space()]

    @staticmethod
    def __create_default_space() -> UserCloudSpace:
        return UserCloudSpace(
            space_type=SpaceType.Regular,
        )

    def create_space_by_directory(self, directory: Directory, space_type=SpaceType.Shared):
        if isinstance(directory, Directory):
            directory_manager = DirectoryManager(
                file_manager=None,
                items=[directory]
            )
            new_space = UserCloudSpace(
                space_type=space_type,
                directory_manager=directory_manager
            )
            self.__spaces.append(new_space)
        else:
            raise TypeError

    def create_space_by_file(self, file: File, space_type=SpaceType.Shared):
        if isinstance(file, File):
            file_manager = FileManager(
                items=[file]
            )
            directory_manager = DirectoryManager(
                file_manager=file_manager,
                items=None
            )
            new_space = UserCloudSpace(
                space_type=space_type,
                directory_manager=directory_manager
            )
            self.__spaces.append(new_space)
        else:
            raise TypeError

    def remove_cloud_space(self, space_id: uuid.UUID):
        if isinstance(space_id, uuid.UUID):
            for space in self.__spaces:
                if space.get_id() == space_id:
                    self.__spaces.remove(space)
                    return
            else:
                raise ValueError
        else:
            raise TypeError

    def get_spaces(self) -> list[UserCloudSpace]:
        return self.__spaces

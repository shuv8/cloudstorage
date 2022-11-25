import uuid
from enum import Enum
from typing import Optional

from cloud_storage_service.directory_manager import DirectoryManager


class SpaceType(Enum):
    Regular = 1
    Complaint = 2
    Shared = 3


class UserCloudSpace:
    def __init__(
            self,
            space_type: SpaceType,
            _id: uuid.UUID = uuid.uuid4(),
            directory_manager: Optional[DirectoryManager] = None
    ):
        self.__directory_manager: DirectoryManager = directory_manager or DirectoryManager(file_manager=None, items=None)
        self.__space_id = _id
        self.__spaceType = space_type

    def get_id(self) -> uuid.UUID:
        return self.__space_id

    def get_space_type(self) -> SpaceType:
        return self.__spaceType

    def get_directory_manager(self) -> Optional[DirectoryManager]:
        return self.__directory_manager

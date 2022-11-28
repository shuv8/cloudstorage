from enum import Enum
from typing import Optional, BinaryIO
from uuid import UUID

from core.accesses import BaseAccess
from core.base_storage_item import BaseStorageItem
from core.files import File
from exceptions.exceptions import NotAllowedError, ItemNotFoundError
from service.data_store_service import DataStoreService
from service.access_service import AccessService


class AccessEditTypeEnum(Enum):
    Add = 1
    Remove = 2


class AccessClassEnum(Enum):
    Url = 1
    UserEmail = 2
    Department = 3


class DataStoreController:

    def __init__(self):
        self.data_store_service = DataStoreService()
        self.access_service = AccessService()

    """
        ==================
        Data Store Service
        ==================
    """

    def search_in_cloud(self, user_mail: str, file_name: str) -> list[tuple[BaseStorageItem, str]]:
        return self.data_store_service.search_in_cloud(user_mail, file_name)

    def rename_item(self, user_mail: str, item_id: UUID, new_name: str):
        return self.data_store_service.rename_item_by_id(item_id=item_id, user_mail=user_mail, new_name=new_name)

    def move_item(self, user_mail: str, item_id: UUID, target_directory_id: UUID):
        return self.data_store_service.move_item(item_id=item_id, user_mail=user_mail, target_directory_id=target_directory_id)

    def get_item_by_id(self, user_mail: str, item_id: UUID) -> Optional[BaseStorageItem]:
        return self.data_store_service.get_user_file_by_id(user_mail, item_id)

    def download_item(self, item_id: UUID) -> [Optional[BinaryIO], File]:
        return self.data_store_service.download_item(user_mail="test", item_id=item_id)

    def delete_item(self, item_id: UUID) -> bool:
        return self.data_store_service.delete_item(user_mail="test", item_id=item_id)

    def copy_item(self, user_mail: str, item_id: UUID, target_directory_id: UUID):
        return self.data_store_service.copy_item(item_id=item_id, user_mail=user_mail, target_directory_id=target_directory_id)

    """
        ==============
        Access Service
        ==============
    """

    def get_accesses(self, item_id: UUID) -> list[BaseAccess]:
        return self.access_service.get_accesses_for_item(item_id)

    def edit_access(
            self,
            item_id: UUID,
            edit_type: AccessEditTypeEnum,
            access_class: AccessClassEnum,
            view_only: Optional[bool] = True,
            name: Optional[str] = None,
    ):
        try:
            if edit_type == AccessEditTypeEnum.Add:
                if access_class == AccessClassEnum.Url:
                    self.access_service.add_access_for_item_by_url(item_id, view_only)
                if access_class == AccessClassEnum.UserEmail:
                    self.access_service.add_access_for_item_by_email(item_id, name, view_only)
                if access_class == AccessClassEnum.Department:
                    self.access_service.add_access_for_item_by_department(item_id, name, view_only)
                return True
            elif edit_type == AccessEditTypeEnum.Remove:
                if access_class == AccessClassEnum.Url:
                    self.access_service.remove_access_for_item_by_url(item_id)
                if access_class == AccessClassEnum.UserEmail:
                    self.access_service.remove_access_for_item_by_email(item_id, name)
                if access_class == AccessClassEnum.Department:
                    self.access_service.remove_access_for_item_by_department(item_id, name)
                return True
            else:
                return False
        except NotAllowedError:
            raise NotAllowedError
        except ItemNotFoundError:
            raise ItemNotFoundError

from enum import Enum
from typing import Optional
from uuid import UUID

from core.accesses import BaseAccess
from core.base_storage_item import BaseStorageItem
from exceptions.exceptions import NotAllowedError
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

    def rename_item(self, item_id: UUID, new_name: str):
        return self.data_store_service.rename_item_by_id(item_id=item_id, user_mail='test', new_name=new_name)

    def move_item(self, item_id: UUID, target_directory_id: UUID):
        return self.data_store_service.move_item(item_id=item_id, user_mail='test', target_directory_id=target_directory_id)

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
            view_only: Optional[bool] = None,
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

import uuid
from uuid import UUID

from core.accesses import UrlAccess, Access, UserAccess, DepartmentAccess, BaseAccess
from decorators.token_required import get_user_by_token
from exceptions.exceptions import NotAllowedError
from service.data_store_service import DataStoreService


class AccessService:

    def __init__(self):
        self.data_store_service = DataStoreService()

    def get_accesses_for_item(self, item_id: UUID) -> list[BaseAccess]:
        user = get_user_by_token()
        if not self.data_store_service.is_user_item(user.email, item_id):
            raise NotAllowedError()
        else:
            item = self.data_store_service.get_user_item_by_id(user.email, item_id)

        return self.data_store_service.get_accesses_for_item(item)

    def add_access_for_item_by_url(self, item_id: UUID, view_only: bool) -> str:
        user = get_user_by_token()
        if not self.data_store_service.is_user_item(user.email, item_id):
            raise NotAllowedError()
        else:
            item = self.data_store_service.get_user_item_by_id(user.email, item_id)

        if view_only:
            access_type = Access.View
        else:
            access_type = Access.Edit

        new_access = UrlAccess(
            url=str(uuid.uuid4()),
            access_type=access_type
        )

        return self.data_store_service.set_url_access_for_item(item, new_access)

    def remove_access_for_item_by_url(self, item_id: UUID) -> str:
        user = get_user_by_token()
        if not self.data_store_service.is_user_item(user.email, item_id):
            raise NotAllowedError()
        else:
            item = self.data_store_service.get_user_item_by_id(user.email, item_id)

        return self.data_store_service.remove_url_access_for_item(item)

    def add_access_for_item_by_email(self, item_id: UUID, email: str, view_only: bool) -> str:
        user = get_user_by_token()
        if not self.data_store_service.is_user_item(user.email, item_id):
            raise NotAllowedError()
        else:
            item = self.data_store_service.get_user_item_by_id(user.email, item_id)

        if view_only:
            access_type = Access.View
        else:
            access_type = Access.Edit

        new_access = UserAccess(
            email=email,
            access_type=access_type
        )

        return self.data_store_service.add_email_access_for_item(item, new_access)

    def remove_access_for_item_by_email(self, item_id: UUID, email: str) -> str:
        user = get_user_by_token()
        if not self.data_store_service.is_user_item(user.email, item_id):
            raise NotAllowedError()
        else:
            item = self.data_store_service.get_user_item_by_id(user.email, item_id)

        return self.data_store_service.remove_email_access_for_item(item, email)

    def add_access_for_item_by_department(self, item_id: UUID, department: str, view_only: bool) -> str:
        user = get_user_by_token()
        if not self.data_store_service.is_user_item(user.email, item_id):
            raise NotAllowedError()
        else:
            item = self.data_store_service.get_user_item_by_id(user.email, item_id)

        if view_only:
            access_type = Access.View
        else:
            access_type = Access.Edit

        new_access = DepartmentAccess(
            department_name=department,
            access_type=access_type
        )

        return self.data_store_service.add_department_access_for_item(item, new_access)

    def remove_access_for_item_by_department(self, item_id: UUID, department: str) -> str:
        user = get_user_by_token()
        if not self.data_store_service.is_user_item(user.email, item_id):
            raise NotAllowedError()
        else:
            item = self.data_store_service.get_user_item_by_id(user.email, item_id)

        return self.data_store_service.remove_department_access_for_item(item, department)

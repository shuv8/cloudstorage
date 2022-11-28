import uuid
from uuid import UUID

from app_states_for_test import ScopeTypeEnum
from core.accesses import UrlAccess, Access, UserAccess, DepartmentAccess, BaseAccess
from exceptions.exceptions import NotAllowedError
from service.data_store_service import DataStoreService


class AccessService:

    def __init__(self, server_state):
        self.server_state = server_state
        self.data_store_service = DataStoreService(server_state)
        self.scope = ScopeTypeEnum.Prod

    def set_scope(self, scope: ScopeTypeEnum):
        self.scope = scope

    def get_accesses_for_item(self, item_id: UUID) -> list[BaseAccess]:
        user_mail = "test_mail@mail.com"  # TODO NEED REAL USER MAIL FORM AUTH
        if not self.data_store_service.is_user_file(user_mail, item_id):
            raise NotAllowedError()

        return self.data_store_service.get_accesses_for_item(user_mail, item_id)

    def add_access_for_item_by_url(self, item_id: UUID, view_only: bool):
        user_mail = "test_mail@mail.com"  # TODO NEED REAL USER MAIL FORM AUTH
        if not self.data_store_service.is_user_file(user_mail, item_id):
            raise NotAllowedError()

        if view_only:
            access_type = Access.View
        else:
            access_type = Access.Edit

        new_access = UrlAccess(
            url=str(uuid.uuid4()),  # TODO MAKE IT STRONGER
            access_type=access_type
        )

        self.data_store_service.set_url_access_for_file(user_mail, item_id, new_access)

    def remove_access_for_item_by_url(self, item_id: UUID):
        user_mail = "test_mail@mail.com"  # TODO NEED REAL USER MAIL FORM AUTH
        if not self.data_store_service.is_user_file(user_mail, item_id):
            raise NotAllowedError()

        self.data_store_service.remove_url_access_for_file(user_mail, item_id)

    def add_access_for_item_by_email(self, item_id: UUID, email: str, view_only: bool):
        user_mail = "test_mail@mail.com"  # TODO NEED REAL USER MAIL FORM AUTH
        if not self.data_store_service.is_user_file(user_mail, item_id):
            raise NotAllowedError()

        if view_only:
            access_type = Access.View
        else:
            access_type = Access.Edit

        new_access = UserAccess(
            email=email,
            access_type=access_type
        )

        self.data_store_service.add_email_access_for_file(user_mail, item_id, new_access)

    def remove_access_for_item_by_email(self, item_id: UUID, email: str):
        user_mail = "test_mail@mail.com"  # TODO NEED REAL USER MAIL FORM AUTH
        if not self.data_store_service.is_user_file(user_mail, item_id):
            raise NotAllowedError()

        self.data_store_service.remove_email_access_for_file(user_mail, item_id, email)

    def add_access_for_item_by_department(self, item_id: UUID, department: str, view_only: bool):
        user_mail = "test_mail@mail.com"  # TODO NEED REAL USER MAIL FORM AUTH
        if not self.data_store_service.is_user_file(user_mail, item_id):
            raise NotAllowedError()

        if view_only:
            access_type = Access.View
        else:
            access_type = Access.Edit

        new_access = DepartmentAccess(
            department_name=department,
            access_type=access_type
        )

        self.data_store_service.add_department_access_for_file(user_mail, item_id, new_access)

    def remove_access_for_item_by_department(self, item_id: UUID, department: str):
        user_mail = "test_mail@mail.com"  # TODO NEED REAL USER MAIL FORM AUTH
        if not self.data_store_service.is_user_file(user_mail, item_id):
            raise NotAllowedError()

        self.data_store_service.remove_department_access_for_file(user_mail, item_id, department)

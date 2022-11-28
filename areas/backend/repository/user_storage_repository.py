from typing import List

from uuid import UUID

from app_states_for_test import ScopeTypeEnum
from core.user import User
from core.department import Department


class UserRepository:
    def __init__(self, server_state):
        self.server_state = server_state
        self.scope = ScopeTypeEnum.Prod

    def set_scope(self, scope: ScopeTypeEnum):
        self.scope = scope

    def get_user(self, id: UUID) -> User:
        return self.server_state.get_user(id)

    def get_user_by_email(self, email: str) -> User:
        return self.server_state.get_user_by_email(email)

    def add_new_user(self, new_user: User) -> None:
        self.server_state.add_new_user(new_user)

    def get_departments(self) -> List[Department]:
        return self.server_state.get_department_list()

    def get_department_by_name(self, department_name) -> Department:
        return self.server_state.get_department_by_name(department_name)

    def add_new_department(self, new_department: Department) -> None:
        self.server_state.add_new_department(new_department)

    def delete_department_by_name(self, department_name: str) -> None:
        self.server_state.delete_department_by_name(department_name)

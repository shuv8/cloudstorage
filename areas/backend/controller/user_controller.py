from typing import List

from app_states_for_test import ScopeTypeEnum
from core.department import Department
from core.role import Role
from core.user import User
from service.user_service import UserService


class UserController:

    def __init__(self, server_state):
        self.server_state = server_state
        self.user_service = UserService(server_state)
        self.scope = ScopeTypeEnum.Prod

    def set_scope(self, scope: ScopeTypeEnum):
        self.scope = scope
        self.user_service.set_scope(scope)

    def registration(self, email: str, password: str, role: Role, username: str) -> None:
        self.user_service.registration(email, password, role, username)

    def login(self, email: str, password: str) -> str:
        return self.user_service.login(email, password)

    def authentication(self, token: str) -> User:
        return self.user_service.authentication(token)

    def get_all_departments(self, page: int, limit: int) -> List[Department]:
        return self.user_service.get_all_departments(page, limit)

    def add_new_department(self, new_department: Department) -> None:
        self.user_service.add_new_department(new_department)

    def delete_department_by_name(self, department_name: str) -> None:
        self.user_service.delete_department_by_name(department_name)

    def get_department_by_name(self, department_name: str) -> Department:
        return self.user_service.get_department_by_name(department_name)

    def add_users_to_department(self, department_name: str, users: List[str]) -> Department:
        return self.user_service.add_users_to_department(department_name, users)

    def delete_users_from_department(self, department_name: str, users: List[str]) -> Department:
        return self.user_service.delete_users_from_department(department_name, users)

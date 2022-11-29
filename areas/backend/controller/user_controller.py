from typing import List

from app_states_for_test import ScopeTypeEnum
from core.department import Department
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

    def registration(self, new_user: User) -> None:
        self.user_service.registration(new_user)

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

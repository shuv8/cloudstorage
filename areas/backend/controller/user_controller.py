from typing import Optional, List

from core.department import Department
from core.user import User
from service.user_service import UserService


class UserController:
    def __init__(self):
        self.user_service = UserService()

    def registration(self, new_user: User) -> Optional[str]:
        return self.user_service.registration(new_user)

    def login(self, email: str, password: str):
        return self.user_service.login(email, password)

    def get_all_departments(self, page: int, limit: int) -> List[Department]:
        return self.user_service.get_all_departments(page, limit)

    def add_new_department(self, new_department: Department) -> None:
        self.user_service.add_new_department(new_department)

    def delete_department_by_name(self, department_name: str) -> None:
        self.user_service.delete_department_by_name(department_name)

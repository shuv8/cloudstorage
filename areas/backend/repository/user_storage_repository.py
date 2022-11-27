from typing import Optional, List

from core.user import User
from database.directories_mock import DataBaseTemporaryMock
from core.department import Department


class UserRepository:
    db = DataBaseTemporaryMock()

    def create_user(self, new_user: User):
        self.db.create_user(new_user)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.get_user_by_email(email)

    def get_departments(self) -> List[Department]:
        return self.db.get_department_list()

    def get_department_by_name(self, department_name) -> Department:
        return self.db.get_department_by_name(department_name)

    def add_new_department(self, new_department: Department) -> None:
        self.db.add_new_department(new_department)

    def delete_department_by_name(self, department_name: str) -> None:
        self.db.delete_department_by_name(department_name)

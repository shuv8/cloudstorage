import bcrypt
import jwt
from typing import List

from core.department import Department
from core.department_manager import DepartmentNotFoundError
from exceptions.exceptions import AlreadyExistsError
from core.user import User
from repository.user_storage_repository import UserRepository


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def registration(self, new_user: User):
        if self.user_repo.get_user_by_email(new_user.email):
            return "email already exist"

        salt = bcrypt.gensalt()
        new_user.password = bcrypt.hashpw(
            new_user.password.encode(), salt).decode()

        return self.user_repo.create_user(new_user)

    def login(self, email: str, password: str):
        user = self.user_repo.get_user_by_email(email)

        if not user:
            return None, "incorrect email or password"

        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            return None, "incorrect email or password"

        token = jwt.encode({"email": user.email, "hash": user.password},
                           "SUPER-SECRET-KEY", algorithm="HS256")  # TODO: get secret from env

        return token, None

    def get_all_departments(self, page: int, limit: int) -> List[Department]:
        departments = self.user_repo.get_departments()
        output_list = []
        start_index = (page - 1) * limit
        end_index = min(len(departments), start_index + limit)
        for index in range(start_index, end_index):
            output_list.append(departments[index])
        return output_list

    def add_new_department(self, new_department: Department) -> None:
        try:
            self.user_repo.get_department_by_name(new_department.department_name)
            raise AlreadyExistsError
        except DepartmentNotFoundError:
            self.user_repo.add_new_department(new_department)

    def delete_department_by_name(self, department_name: str) -> None:
        self.user_repo.delete_department_by_name(department_name)


from typing import List

from bcrypt import checkpw, gensalt, hashpw
from jwt import encode

from core.department import Department
from core.department_manager import DepartmentNotFoundError
from core.user_manager import UserNotFoundError
from exceptions.exceptions import AlreadyExistsError, InvalidCredentialsError
from core.user import User
from repository.user_storage_repository import UserRepository


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def registration(self, new_user: User) -> None:
        try:
            self.user_repo.get_user_by_email(new_user.email)
            raise AlreadyExistsError
        except UserNotFoundError:
            hash = hashpw(
                str(new_user.password).encode(), gensalt()
            )
            new_user.password = hash.decode()
            self.user_repo.add_new_user(new_user)

    def login(self, email: str, password: str) -> str:
        try:
            user = self.user_repo.get_user_by_email(email)
            print(user.email)
            if checkpw(password.encode(), str(user.password).encode()) is False:
                raise InvalidCredentialsError
            # TODO: get secret from env
            token = encode({"id": str(user.get_id())}, "SUPER-SECRET-KEY", algorithm="HS256")  
            return token
        except UserNotFoundError:
            raise InvalidCredentialsError

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


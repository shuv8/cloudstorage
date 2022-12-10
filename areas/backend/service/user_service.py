from typing import List
from uuid import UUID

from bcrypt import checkpw, gensalt, hashpw
from jwt import InvalidTokenError, decode, encode

from app_states_for_test import ScopeTypeEnum
from core.accesses import Access, BaseAccess
from core.department import Department
from core.department_manager import DepartmentNotFoundError
from core.directory import Directory
from core.directory_manager import DirectoryManager
from core.files import FileManager
from core.role import Role
from core.space_manager import SpaceManager
from core.user_cloud_space import SpaceType, UserCloudSpace
from core.user_manager import UserNotFoundError
from exceptions.exceptions import AlreadyExistsError, InvalidCredentialsError
from core.user import User
from repository.user_storage_repository import UserRepository


class UserService:
    def __init__(self, server_state):
        self.server_state = server_state
        self.user_repo = UserRepository(server_state)
        self.scope = ScopeTypeEnum.Prod

    def set_scope(self, scope: ScopeTypeEnum):
        self.scope = scope
        self.user_repo.set_scope(scope)

    def registration(self, email: str, password: str, role: Role, username: str) -> None:
        try:
            self.user_repo.get_user_from_db_by_email(email)
            raise AlreadyExistsError
        except UserNotFoundError:
            directory = Directory(
                accesses=[
                    BaseAccess(access_type=Access.View),
                    BaseAccess(access_type=Access.Edit),
                ],
                name="root"
            )
            directory_manager = DirectoryManager(
                items=[directory],
                file_manager=FileManager(
                    items=[]
                )
            )
            space = UserCloudSpace(
                space_type=SpaceType.Regular,
                directory_manager=directory_manager
            )
            space_manager = SpaceManager(
                spaces=[space]
            )
            new_user = User(
                email=email,
                password=password,
                role=role,
                username=username,
                space_manager=space_manager
            )
            hash = hashpw(
                str(new_user.password).encode(), gensalt()
            )
            new_user.password = hash.decode()
            self.user_repo.add_new_user_to_db(new_user)

    def login(self, email: str, password: str) -> str:
        try:
            user = self.user_repo.get_user_from_db_by_email(email)
            if checkpw(password.encode(), str(user.password).encode()) is False:
                raise InvalidCredentialsError
            # TODO: get secret from env
            token = encode({"id": str(user.get_id())}, "SUPER-SECRET-KEY", algorithm="HS256")  
            return token
        except UserNotFoundError:
            raise InvalidCredentialsError

    def authentication(self, token: str) -> User:
        try:
            payload = decode(token, "SUPER-SECRET-KEY", ["HS256"])
            _id = UUID(hex=payload["id"])
            return self.user_repo.get_user_from_db_by_id(_id)
        except:
            raise InvalidTokenError

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

    def get_department_by_name(self, department_name: str) -> Department:
        return self.user_repo.get_department_by_name(department_name)

    def add_users_to_department(self, department_name: str, users: List[str]) -> Department:
        department = self.user_repo.get_department_by_name(department_name)
        new_users = []
        for user in users:
            new_users.append(self.user_repo.get_user_from_db_by_id(UUID(user)))
        old_users = department.users
        updated_users = old_users + new_users
        department.users = updated_users
        new_department = self.user_repo.update_department_users(department)
        return new_department

    def delete_users_from_department(self, department_name: str, users: List[str]) -> Department:
        department = self.user_repo.get_department_by_name(department_name)
        new_users = []
        for user in department.users:
            if str(user.get_id()) not in users:
                new_users.append(user)
        department.users = new_users
        new_department = self.user_repo.update_department_users(department)
        return new_department

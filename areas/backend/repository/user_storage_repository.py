import sys
from typing import List
from uuid import UUID

from accessify import private

from app_state import ServerDatabase
from app_states_for_test import ScopeTypeEnum
from core.user import User
from core.department import Department
from flask import current_app
from core.user_manager import UserNotFoundError
from app_db import get_current_db


db = get_current_db(current_app)


class UserRepository:
    def __init__(self, server_state: ServerDatabase):
        self.server_state = server_state.prod
        self.test_server_state = server_state.test
        self.scope = ScopeTypeEnum.Prod

    """
        New methods
    """

    def get_user_from_db_by_id(self, _id: UUID):
        from database.users.user_model import UserModel
        user: UserModel = UserModel.query.filter_by(id=str(_id)).first()
        if user is None:
            raise UserNotFoundError
        return User(
            _id=UUID(hex=user.id),
            email=user.email,
            username=user.username,
            password=user.passwordHash,
            role=user.role
        )

    def get_user_from_db_by_email(self, email: str) -> User:
        from database.users.user_model import UserModel
        user: UserModel = UserModel.query.filter_by(email=email).first()
        if user is None:
            raise UserNotFoundError
        return User(
            _id=UUID(hex=user.id),
            email=user.email,
            username=user.username,
            password=user.passwordHash,
            role=user.role
        )

    def add_new_user_to_db(self, new_user: User) -> None:
        from database.users.user_model import UserModel, UserSpaceModel, DirectoryModel
        space_manager = new_user.get_space_manager()
        root_space = space_manager.get_spaces()[0]
        directory_manager = root_space.get_directory_manager()
        root_directory = directory_manager.get_items()[0]
        directory: DirectoryModel = DirectoryModel(
            id=str(root_directory.get_id()),
            name="root",
            is_root=True,
        )
        space: UserSpaceModel = UserSpaceModel(
            id=str(root_space.get_id()),
            space_type=root_space.get_space_type(),
        )
        space.root_directory = directory
        user: UserModel = UserModel(
            id=str(new_user.get_id()),
            email=new_user.email,
            username=new_user.username,
            passwordHash=new_user.password,
            role=new_user.role
        )
        user.spaces.append(space)

        db.session.add(user)
        db.session.add(space)
        db.session.add(directory)
        db.session.commit()

    """
        Old methods
    """

    @private
    def get_db(self):
        if "pytest" in sys.modules:
            return ScopeTypeEnum.return_state_by_scope(self.scope, self.server_state, self.test_server_state)
        else:
            return self.server_state

    def set_scope(self, scope: ScopeTypeEnum):
        self.scope = scope

    def get_user(self, id: UUID) -> User:
        return self.get_db().get_user(id)

    def get_user_by_email(self, email: str) -> User:
        return self.get_db().get_user_by_email(email)

    def add_new_user(self, new_user: User) -> None:
        self.get_db().add_new_user(new_user)

    def get_departments(self) -> List[Department]:
        from database.users.user_model import DepartmentModel
        departments: List[DepartmentModel] = DepartmentModel.query.all()
        departments_list = [Department(i.name, None) for i in departments]
        return departments_list

    def get_department_by_name(self, department_name) -> Department:
        from database.users.user_model import DepartmentModel
        from core.department_manager import DepartmentNotFoundError
        department: DepartmentModel = DepartmentModel.query.filter_by(name=department_name).first()
        if department is None:
            raise DepartmentNotFoundError
        users = [
            User(
                _id=UUID(hex=user.id),
                email=user.email,
                username=user.username,
                password=user.passwordHash,
                role=user.role
            )
            for user in department.users
        ]
        return Department(
            department_name=department.name,
            users=users
        )

    def add_new_department(self, new_department: Department) -> None:
        from database.users.user_model import DepartmentModel
        department: DepartmentModel = DepartmentModel(name=new_department.department_name)
        db.session.add(department)
        db.session.commit()

    def delete_department_by_name(self, department_name: str) -> None:
        from database.users.user_model import DepartmentModel
        from core.department_manager import DepartmentNotFoundError
        department: DepartmentModel = DepartmentModel.query.filter_by(name=department_name).first()
        if department is None:
            raise DepartmentNotFoundError
        db.session.delete(department)
        db.session.commit()

    def update_department_users(self, department: Department) -> None:
        from database.users.user_model import DepartmentModel, UserModel
        from core.department_manager import DepartmentNotFoundError
        department_model: DepartmentModel = DepartmentModel.query.filter_by(name=department.department_name).first()
        if department_model is None:
            raise DepartmentNotFoundError
        users = []
        for user in department.users:
            user_model: UserModel = UserModel.query.filter_by(id=str(user.get_id())).first()
            users.append(user_model)
        department_model.users = users
        db.session.commit()
        return self.get_department_by_name(department.department_name)

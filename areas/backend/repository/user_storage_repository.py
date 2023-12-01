from typing import List
from uuid import UUID

from areas.backend.core.accesses import AccessType
from areas.backend.core.department_manager import DepartmentManager
from areas.backend.core.user import User
from areas.backend.core.department import Department
from flask import current_app
from areas.backend.core.user_manager import UserNotFoundError
from areas.backend.app_db import get_current_db
from areas.backend.repository.data_store_storage_repository import DataStoreStorageRepository

db = get_current_db(current_app)


class UserRepository:
    """
        New methods
    """

    def __init__(self):
        self.data_storage_repo = DataStoreStorageRepository()

    def get_user_from_db_by_id(self, _id: UUID):
        from areas.backend.database.database import UserModel
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

    def get_user_from_db_by_id(self, _id: UUID):
        from areas.backend.database.database import UserModel, DepartmentModel
        user: UserModel = UserModel.query.filter_by(id=str(_id)).first()
        if user is None:
            raise UserNotFoundError
        current_user = User(
            _id=UUID(hex=user.id),
            email=user.email,
            username=user.username,
            password=user.passwordHash,
            role=user.role,
            _department_manager=DepartmentManager([])
        )

        department: DepartmentModel = DepartmentModel.query.filter_by(id=user.department_id).first()
        if department is not None:
            current_user.department_manager.add_department(
                Department(
                    department_name=department.name,
                    users=[]
                )
            )

        return current_user

    def get_user_departments_by_id(self, _id: UUID) -> list[str]:
        from areas.backend.database.database import UserModel
        user: UserModel = UserModel.query.filter_by(id=str(_id)).first()
        return [department.name for department in user.departments]


    def get_user_from_db_by_email(self, email: str) -> User:
        from areas.backend.database.database import UserModel
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

    @staticmethod
    def add_new_user_to_db(new_user: User) -> None:
        from areas.backend.database.database import UserModel

        user: UserModel = UserModel(
            id=str(new_user.get_id()),
            email=new_user.email,
            username=new_user.username,
            passwordHash=new_user.password,
            role=new_user.role
        )

        db.session.add(user)
        db.session.commit()

    """
        Old methods
    """

    def get_departments(self) -> List[Department]:
        from areas.backend.database.database import DepartmentModel
        departments: List[DepartmentModel] = DepartmentModel.query.all()
        departments_list = [Department(i.name, i.users) for i in departments]
        return departments_list

    def get_users(self) -> List[User]:
        from areas.backend.database.database import UserModel
        users: List[UserModel] = UserModel.query.all()
        all_users = [
            User(
                _id=UUID(hex=user.id),
                email=user.email,
                username=user.username,
                password=user.passwordHash,
                role=user.role
            )
            for user in users
        ]
        return all_users

    def get_department_by_name(self, department_name) -> Department:
        from areas.backend.database.database import DepartmentModel
        from areas.backend.core.department_manager import DepartmentNotFoundError
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
        from areas.backend.database.database import DepartmentModel
        department: DepartmentModel = DepartmentModel(name=new_department.department_name)
        db.session.add(department)
        db.session.commit()

    def delete_department_by_name(self, department_name: str) -> None:
        from areas.backend.database.database import DepartmentModel
        from areas.backend.core.department_manager import DepartmentNotFoundError
        department: DepartmentModel = DepartmentModel.query.filter_by(name=department_name).first()
        if department is None:
            raise DepartmentNotFoundError
        db.session.delete(department)
        db.session.commit()

    def update_department_users(self, department: Department) -> Department:
        from areas.backend.database.database import DepartmentModel, UserModel
        department_model: DepartmentModel = DepartmentModel.query.filter_by(name=department.department_name).first()
        users = []
        for user in department.users:
            user_model: UserModel = UserModel.query.filter_by(id=str(user.get_id())).first()
            users.append(user_model)
        department_model.users = users
        db.session.commit()
        return self.get_department_by_name(department.department_name)

    @staticmethod
    def remove_users_accesses(users_ids: List[str], department_name: str):
        from areas.backend.database.database import UserModel

        for user in users_ids:
            user_model: UserModel = UserModel.query.filter_by(id=user).first()
            if user_model is not None:
                for space in user_model.spaces:
                    if space.root_directory.is_root:
                        for access in space.root_directory.files[0].accesses:
                            if access.access_type == AccessType.Department:
                                if access.value == department_name:
                                    user_model.spaces.remove(space)
                    else:
                        for access in space.root_directory.accesses:
                            if access.access_type == AccessType.Department:
                                if access.value == department_name:
                                    user_model.spaces.remove(space)

        db.session.commit()

    def add_users_accesses(self, users_ids: List[str], department_name: str):
        from areas.backend.database.database import AccessModel, FileModel, DirectoryModel, UserModel

        accesses: list[AccessModel] = AccessModel.query.filter(
            (AccessModel.access_type == AccessType.Department) & (AccessModel.value == department_name)
        ).all()

        for access in accesses:
            if access.parent_file_id is not None:
                file: FileModel = FileModel.query.filter_by(id=access.parent_file_id).first()
                for user_id in users_ids:
                    user_model: UserModel = UserModel.query.filter_by(id=user_id).first()
                    if user_model is not None:
                        self.data_storage_repo.add_shared_space_for_file_model_by_email(file, user_model.email)
            elif access.parent_id is not None:
                directory: DirectoryModel = DirectoryModel.query.filter_by(id=access.parent_id).first()
                for user_id in users_ids:
                    user_model: UserModel = UserModel.query.filter_by(id=user_id).first()
                    if user_model is not None:
                        self.data_storage_repo.add_shared_space_for_directory_model_by_email(directory,
                                                                                             user_model.email)

    def get_root_user_space_content(self, user_email: str):
        return self.data_storage_repo.get_root_user_space_content(user_email)

import base64
import sys
import uuid
from typing import BinaryIO, Optional

from accessify import private
from sqlalchemy import update
from sqlalchemy import delete

from app_state import ServerDatabase
from app_states_for_test import ScopeTypeEnum
from core.accesses import BaseAccess, UrlAccess, AccessType, DepartmentAccess, UserAccess
from core.base_storage_item import BaseStorageItem
from core.directory import Directory
from core.files import File
from core.space_manager import SpaceManager
from core.user_cloud_space import UserCloudSpace
from flask import current_app
from app_db import get_current_db

from database.users.user_model import FileModel, UserModel, UserSpaceModel, DirectoryModel, AccessModel


class DataStoreStorageRepository:
    def __init__(self, server_state: ServerDatabase):
        self.server_state = server_state.prod
        self.test_server_state = server_state.test
        self.scope = ScopeTypeEnum.Prod
        self.db = get_current_db(current_app)

    def set_scope(self, scope: ScopeTypeEnum):
        self.scope = scope

    def get_user_spaces(self, user_mail: str) -> list[UserCloudSpace]:
        return self.get_root_dir_by_user_mail(user_mail).get_spaces()

    def get_user_space_content(self, user_mail: str, space_id: uuid.UUID) -> Optional[UserCloudSpace]:
        spaces: list[UserCloudSpace] = self.get_user_spaces(user_mail)
        for space in spaces:
            if space.get_id() == space_id:
                return space

    @private
    def get_db(self):
        if "pytest" in sys.modules:
            return ScopeTypeEnum.return_state_by_scope(self.scope, self.server_state, self.test_server_state)
        else:
            return self.server_state

    def add_new_file(self, user_email: str, space_id: uuid.UUID, dir_id: uuid.UUID, new_file: File,
                     new_file_data: str) -> uuid.UUID:
        file_id = self.get_db().add_new_file(user_email, space_id, dir_id, new_file)
        with open(f'storage/{file_id}{new_file.get_type()}', "wb") as fh:
            fh.write(base64.decodebytes(str.encode(new_file_data)))
        return file_id

    def get_file_by_item_id(self, item_id: uuid.UUID) -> SpaceManager:
        return self.get_db().get_file_by_item_id(item_id)

    def fill_directory_with_data(self, directory: DirectoryModel) -> Directory:
        partly_root_directory = Directory(
            _id=uuid.UUID(directory.id),
            name=directory.name,
        )

        files_in_directory: list[File] = []
        for file in directory.files:

            accesses: list[BaseAccess] = []
            for access in file.accesses:
                if access.access_type == AccessType.Url:
                    accesses.append(
                        UrlAccess(
                            url=access.value,
                            access_type=access.access_level
                        )
                    )
                if access.access_type == AccessType.User:
                    accesses.append(
                        UserAccess(
                            email=access.value,
                            access_type=access.access_level
                        )
                    )
                if access.access_type == AccessType.Department:
                    accesses.append(
                        DepartmentAccess(
                            department_name=access.value,
                            access_type=access.access_level
                        )
                    )

            files_in_directory.append(
                File(
                    name=file.name,
                    _id=file.id,
                    _type=file.type,
                    accesses=accesses
                )
            )

        inner_directories: list[Directory] = []
        for inner_directory in directory.inner_directories:
            inner_directories.append(self.fill_directory_with_data(inner_directory))

        partly_root_directory.get_directory_manager().items = inner_directories
        partly_root_directory.get_directory_manager().file_manager.items = files_in_directory

        return partly_root_directory

    def get_root_dir_by_user_mail(self, user_mail: str) -> SpaceManager:

        user: UserModel = UserModel.query.filter_by(email=user_mail).first()
        user_space_models: list[UserSpaceModel] = UserSpaceModel.query.filter_by(user_id=user.id).all()

        spaces: list[UserCloudSpace] = list()
        for space_model in user_space_models:
            user_cloud = UserCloudSpace(
                _id=uuid.UUID(space_model.id),
                space_type=space_model.space_type
            )

            directory: DirectoryModel = DirectoryModel.query.filter_by(id=space_model.root_directory.id).first()

            root_directory = self.fill_directory_with_data(directory)

            user_cloud.get_directory_manager().items = [root_directory]

            spaces.append(
                user_cloud
            )

        space_manager = SpaceManager(
            spaces=spaces
        )

        return space_manager

    def copy_file(self, file):
        new_id = uuid.uuid4()
        self.server_state.user_cloud_space_1_.get_directory_manager().file_manager.add_item(
            File(
                name="test_copy",
                _type=".txt",
                _id=new_id)
        )
        # TODO: разобраться с айдишниками и их сравнением
        return new_id  # return new file id

    def edit_item_name(self, item):
        if isinstance(item, File):
            self.db.session.execute(update(FileModel).where(FileModel.id == str(item.id)).values(name=item.name))
        elif isinstance(item, Directory):
            self.db.session.execute(
                update(DirectoryModel).where(DirectoryModel.id == str(item.id)).values(name=item.name))
        self.db.session.commit()

    def update_item_access(self, item: BaseStorageItem):
        accesses: list[AccessModel] = []

        for access in item.accesses:
            if type(access) is UrlAccess:
                accesses.append(
                    AccessModel(
                        access_level=access.access_type,
                        access_type=AccessType.Url,
                        value=access.get_url(),
                    )
                )
            elif type(access) is UserAccess:
                accesses.append(
                    AccessModel(
                        access_level=access.access_type,
                        access_type=AccessType.User,
                        value=access.get_email(),
                    )
                )
            elif type(access) is DepartmentAccess:
                accesses.append(
                    AccessModel(
                        access_level=access.access_type,
                        access_type=AccessType.Department,
                        value=access.get_department_name(),
                    )
                )

        if isinstance(item, File):
            file: FileModel = FileModel.query.filter_by(id = str(item.id)).first()
            file.accesses = accesses
        elif isinstance(item, Directory):
            directory: DirectoryModel = DirectoryModel.query.filter_by(id = str(item.id)).first()
            directory.accesses = accesses
        self.db.session.commit()

    def delete_item_from_db(self, item):
        if isinstance(item, File):
            self.db.session.execute(delete(FileModel).where(FileModel.id == str(item.id)))
        elif isinstance(item, Directory):
            self.db.session.execute(
                delete(DirectoryModel).where(DirectoryModel.id == str(item.id)))
        self.db.session.commit()

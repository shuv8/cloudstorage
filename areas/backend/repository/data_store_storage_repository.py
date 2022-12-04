import base64
import sys
import uuid
from typing import BinaryIO, Optional

import pytest
from accessify import private
from sqlalchemy import update

from app_state import ServerDatabase
from app_states_for_test import ScopeTypeEnum
from core.directory import Directory
from core.files import File
from core.space_manager import SpaceManager
from core.user_cloud_space import UserCloudSpace
from flask import current_app
from app_db import get_current_db

from database.users.user_model import FileModel


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
        spaces = self.get_user_spaces(user_mail)
        for space in spaces:
            if space.get_id() == space_id:
                return space_id

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

    def get_root_dir_by_user_mail(self, user_mail: str) -> SpaceManager:
        from database.users.user_model import UserModel, UserSpaceModel, DirectoryModel

        user: UserModel = UserModel.query.filter_by(email=user_mail).first()
        user_space_models: list[UserSpaceModel] = UserSpaceModel.query.filter_by(user_id=user.id).all()

        spaces: list[UserCloudSpace] = list()
        for space_model in user_space_models:
            user_cloud = UserCloudSpace(
                _id=uuid.UUID(space_model.id),
                space_type=space_model.space_type
            )

            root_directory = Directory(
                _id=space_model.root_directory.id,
                name=space_model.root_directory.name,
            )

            directory: DirectoryModel = DirectoryModel.query.filter_by(id=space_model.root_directory.id).first()

            # TODO ВОТ ЭТО ВСЕ ДОЛЖНО ЗАПОЛНЯТЬ ЦИКЛИЧНО, СДЕЛАЙТЕ ПЛИЗ

            files: list[File] = []
            for file in directory.files:
                files.append(
                    File(
                        name=file.name,
                        _id=file.id,
                        _type=file.type
                    )
                )

            dirs: list[Directory] = []
            for directory_ in directory.inner_directories:
                dirs.append(
                    Directory(
                        name=directory_.name,
                        _id=directory_.id,
                    )
                )

            root_directory.get_directory_manager().file_manager.items = files
            root_directory.get_directory_manager().items = dirs

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
            from database.users.user_model import DirectoryModel
            self.db.session.execute(
                update(DirectoryModel).where(DirectoryModel.id == str(item.id)).values(name=item.name))
        self.db.session.commit()

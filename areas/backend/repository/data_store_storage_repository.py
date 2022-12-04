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

db = get_current_db(current_app)


class DataStoreStorageRepository:
    def __init__(self, server_state: ServerDatabase):
        self.server_state = server_state.prod
        self.test_server_state = server_state.test
        self.scope = ScopeTypeEnum.Prod

    def set_scope(self, scope: ScopeTypeEnum):
        self.scope = scope

    def get_user_spaces(self, user_mail: str) -> list[UserCloudSpace]:
        return self.get_db().get_spaces_by_user_mail(user_mail)

    def get_user_space_content(self, user_mail: str, space_id: uuid.UUID) -> Optional[UserCloudSpace]:
        return self.get_db().get_space_content_by_user_mail(user_mail, space_id)

    @private
    def get_db(self):
        if "pytest" in sys.modules:
            return ScopeTypeEnum.return_state_by_scope(self.scope, self.server_state, self.test_server_state)
        else:
            return self.server_state
    
    def add_new_file(self, user_email: str, space_id: uuid.UUID, dir_id: uuid.UUID, new_file: File, new_file_data: str) -> uuid.UUID:
        file_id = self.get_db().add_new_file(user_email, space_id, dir_id, new_file)
        with open(f'storage/{file_id}{new_file.get_type()}', "wb") as fh:
            fh.write(base64.decodebytes(str.encode(new_file_data)))
        return file_id

    def get_file_by_item_id(self, item_id: uuid.UUID) -> SpaceManager:
        return self.get_db().get_file_by_item_id(item_id)

    def get_root_dir_by_user_mail(self, user_mail: str) -> SpaceManager:
        return self.get_db().get_space_manager_by_user_mail(user_mail)

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
            from database.users.user_model import FileModel
            # TODO: temporary adding to db
            if FileModel.query.filter_by(id=str(item.id)).first() is None:
                file: FileModel = FileModel(
                    id = str(item.id),
                    name = item.name,
                    type=item.type
                )
                db.session.add(file)
                db.session.commit()
            # --- end of adding ---
            db.session.execute(update(FileModel).where(FileModel.id == str(item.id)).values(name=item.name))
        elif isinstance(item, Directory):
            from database.users.user_model import DirectoryModel
            db.session.execute(update(DirectoryModel).where(DirectoryModel.id == str(item.id)).values(name=item.name))
        db.session.commit()

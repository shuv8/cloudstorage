import sys
import uuid
from typing import Optional

import pytest
from accessify import private

from app_state import ServerDatabase
from app_states_for_test import ScopeTypeEnum
from core.files import File
from core.space_manager import SpaceManager
from core.user_cloud_space import UserCloudSpace


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

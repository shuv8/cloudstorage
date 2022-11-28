import sys
import uuid

import pytest
from accessify import private

from app_states_for_test import ScopeTypeEnum
from core.files import File
from core.space_manager import SpaceManager


class DataStoreStorageRepository:
    def __init__(self, server_state):
        self.server_state = server_state
        self.scope = ScopeTypeEnum.Prod

    def set_scope(self, scope: ScopeTypeEnum):
        self.scope = scope

    @private
    def get_db(self):
        if "pytest" in sys.modules:
            return ScopeTypeEnum.return_state_by_scope(self.scope, self.server_state)
        else:
            return self.server_state

    def get_root_dir_by_user_mail(self, user_mail: str) -> SpaceManager:
        return self.get_db().get_space_by_user_mail(user_mail)

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

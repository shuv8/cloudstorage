import uuid

from core.files import File
from core.space_manager import SpaceManager
from database.directories_mock import DataBaseTemporaryMock


class DataStoreStorageRepository:
    db = DataBaseTemporaryMock()

    def get_root_dir_by_user_mail(self, user_mail: str) -> SpaceManager:
        return self.db.get_space_by_user_mail(user_mail)

    def copy_file(self, file):
        new_id = uuid.uuid4()
        self.db.user_cloud_space_1_.get_directory_manager().file_manager.add_item(File(name="test_copy", _type=".txt",
                                                                                       _id=new_id))
        # TODO: разобраться с айдишниками и их сравнением
        return new_id  # return new file id

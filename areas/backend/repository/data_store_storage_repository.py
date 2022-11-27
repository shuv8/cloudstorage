from core.space_manager import SpaceManager
from database.directories_mock import DataBaseTemporaryMock


class DataStoreStorageRepository:
    db = DataBaseTemporaryMock()

    def get_root_dir_by_user_mail(self, user_mail: str) -> SpaceManager:
        return self.db.get_space_by_user_mail(user_mail)

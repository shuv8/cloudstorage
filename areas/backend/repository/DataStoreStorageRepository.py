from core.directory import Directory
from database.directories_mock import RootDirectoryForUsersMock


class DataStoreStorageRepository:
    directory_mock = RootDirectoryForUsersMock()

    def get_root_dir_by_user_mail(self, user_mail: str) -> Directory:
        return self.directory_mock.very_mocked_mock(user_mail)

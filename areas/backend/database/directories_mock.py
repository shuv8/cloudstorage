from core.directory import Directory
from core.files import File


class RootDirectoryForUserMock:
    def __init__(self, user_email: str, root_id: str):
        self.user_email = user_email
        self.root_id = root_id


class RootDirectoryForUsersMock:
    dir_to_user = {
        "test_mail@mail.com": 1,
        "test1_mail@mail.com": 2
    }

    def query_by_dir_to_user(self, query: str):
        return self.dir_to_user[query]

    @staticmethod
    def very_mocked_mock(query: str) -> Directory:
        dir_ = Directory(name="test")
        dir_.directory_manager.items = [Directory(name="wow")]
        dir_.directory_manager.file_manager.items = [File(name="wow3", _type=".type"), File(name="test6", _type=".e")]

        return dir_


class ItemInDirectoryMock:
    def __init__(self, directory_id: str, item_id: str):
        self.directory_id = directory_id
        self.item_id = item_id


class ItemInDirectoriesMock:
    data = [
        ItemInDirectoryMock("1", "23"),
        ItemInDirectoryMock("1", "3"),
        ItemInDirectoryMock("3", "25"),
        ItemInDirectoryMock("2", "24"),
    ]

    def query_directory(self, query: str):
        return [item for item in self.data if item.item_id == query]


class DirectoryMock:
    directories = {
        "1": {
            "name": "1",
        },
        "2": {
            "name": "2",
        },
        "3": {
            "name": "3",
        }
    }

    def query_directory(self, query: str):
        return self.directories[query]


class FileMock:
    files = {
        "23": {
            "name": "23",
        },
        "24": {
            "name": "24",
        },
        "25": {
            "name": "25",
        }
    }

    def query_files(self, query: str):
        return self.files[query]

from core.base_storage_item import BaseStorageItem
from core.directory import Directory
from core.files import FileManager, File
from repository.DataStoreStorageRepository import DataStoreStorageRepository
from accessify import private
import logging


class DataStoreService:
    def __init__(self):
        self.data_store_storage_repo = DataStoreStorageRepository()

    def search_in_cloud(self, user_mail: str, query: str) -> list[tuple[BaseStorageItem, str]]:
        root_directory: Directory = self.data_store_storage_repo.get_root_dir_by_user_mail(user_mail)
        founded_items = self.search_in_directory(root=root_directory, query=query)
        return founded_items

    @private
    def search_in_directory(self, root: Directory, query: str, path="/") -> list[tuple[BaseStorageItem, str]]:
        file_and_directories_with_paths = list[tuple[BaseStorageItem, str]]()

        directory_manager = root.directory_manager

        for directory in directory_manager.items:
            if query in directory.name:
                file_and_directories_with_paths.append((directory, path))
            file_and_directories_with_paths.extend(
                self.search_in_directory(
                    root=directory,
                    query=query,
                    path=path + directory.name + "/"
                )
            )

        file_and_directories_with_paths.extend(
            self.search_for_file_in_directory(
                file_manager=root.directory_manager.file_manager,
                query=query,
                path=path
            )
        )

        logging.log(
            level=logging.DEBUG,
            msg=f"For {query} found next items: {[item.name for (item, path) in file_and_directories_with_paths]}"
        )

        return file_and_directories_with_paths

    @private
    def search_for_file_in_directory(self, file_manager: FileManager, query: str, path: str) -> list[tuple[File, str]]:
        files_with_path = [(file, path) for file in file_manager.items if query in file.name]
        return files_with_path

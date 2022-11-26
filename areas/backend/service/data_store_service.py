from typing import Optional
from uuid import UUID

from core.accesses import BaseAccess, DepartmentAccess, UserAccess, UrlAccess
from core.base_storage_item import BaseStorageItem
from core.directory import Directory
from core.files import FileManager, File
from core.space_manager import SpaceManager
from repository.DataStoreStorageRepository import DataStoreStorageRepository
from accessify import private
import logging


class DataStoreService:
    def __init__(self):
        self.data_store_storage_repo = DataStoreStorageRepository()

    def search_in_cloud(self, user_mail: str, query: str) -> list[tuple[BaseStorageItem, str]]:
        """
        @param user_mail: user email
        @param query: query
        """
        space_manager: SpaceManager = self.data_store_storage_repo.get_root_dir_by_user_mail(user_mail)
        founded_items: list[tuple[BaseStorageItem, str]] = self.search_in_spaces(space_manager, query)
        return founded_items

    @private
    def search_in_spaces(self, space_manager: SpaceManager, query: str) -> list[tuple[BaseStorageItem, str]]:
        file_and_directories_with_paths = list[tuple[BaseStorageItem, str]]()
        for space in space_manager.get_spaces():
            for directory in space.get_directory_manager().items:
                file_and_directories_with_paths.extend(
                    self.search_in_directory(directory=directory, query=query, path=f"{space.get_id()}/root/")
                )
                file_and_directories_with_paths.extend(
                    self.search_for_file_in_directory(
                        file_manager=space.get_directory_manager().file_manager,
                        query=query,
                        path=f"{space.get_id()}/root/"
                    )
                )
        return file_and_directories_with_paths

    @private
    def search_in_directory(self, directory: Directory, query: str, path="/") -> list[tuple[BaseStorageItem, str]]:
        file_and_directories_with_paths = list[tuple[BaseStorageItem, str]]()

        if query in directory.name:
            file_and_directories_with_paths.append((directory, path + directory.name + "/"))

        directory_manager = directory.directory_manager

        for directory_ in directory_manager.items:
            if query in directory_.name:
                file_and_directories_with_paths.append((directory_, path))
            file_and_directories_with_paths.extend(
                self.search_in_directory(
                    root=directory_,
                    query=query,
                    path=path + directory_.name + "/"
                )
            )

        file_and_directories_with_paths.extend(
            self.search_for_file_in_directory(
                file_manager=directory.directory_manager.file_manager,
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
    def search_for_file_in_directory(
            self,
            file_manager: FileManager,
            query: str,
            path: str
    ) -> list[tuple[BaseStorageItem, str]]:
        files_with_path = [(file, path + file.name + file.type) for file in file_manager.items if query in file.name]
        return files_with_path

    @private
    def get_item_in_directory_by_id(self, directory: Directory, id_: UUID) -> Optional[BaseStorageItem]:
        if directory.id == id_:
            return directory

        directory_manager = directory.directory_manager

        for directory_ in directory_manager.items:
            if directory_.id == id_:
                return directory_
            item = self.get_item_in_directory_by_id(root=directory_, id_=id_, )
            if item is not None:
                return item

        file = self.get_file_in_directory_by_id(file_manager=directory.directory_manager.file_manager, id_=id_)
        if file is not None:
            return file

        return None

    @private
    def get_file_in_directory_by_id(
            self,
            file_manager: FileManager,
            id_: UUID
    ) -> Optional[BaseStorageItem]:
        for file in file_manager.items:
            if file.id == id_:
                return file
        return None

    def getUserFileById(self, user_mail: str, item_id: UUID) -> Optional[BaseStorageItem]:
        space_manager: SpaceManager = self.data_store_storage_repo.get_root_dir_by_user_mail(user_mail)

        for space in space_manager.get_spaces():
            for directory in space.get_directory_manager().items:

                item = self.get_item_in_directory_by_id(directory=directory, id_=item_id)
                if item is not None:
                    return item

                file = self.get_file_in_directory_by_id(
                    file_manager=space.get_directory_manager().file_manager,
                    id_=item_id
                )
                if file is not None:
                    return file

        return None

    def isUserFile(self, user_mail: str, item_id: UUID) -> bool:
        return self.getUserFileById(user_mail, item_id) is not None

    def set_url_access_for_file(self, user_mail: str, item_id, new_access: BaseAccess):
        item = self.getUserFileById(user_mail, item_id)

        for access in item.accesses:
            if type(access) == UrlAccess:
                return

        item.add_access(new_access)

    def remove_url_access_for_file(self, user_mail: str, item_id: UUID):
        item = self.getUserFileById(user_mail, item_id)

        for access in item.accesses:
            if type(access) == UrlAccess:
                item.accesses.remove(access)
                break

    def add_email_access_for_file(self, user_mail: str, item_id: UUID, new_access: BaseAccess):
        item = self.getUserFileById(user_mail, item_id)
        item.add_access(new_access)

    def remove_email_access_for_file(self, user_mail: str, item_id: UUID, email: str):
        item = self.getUserFileById(user_mail, item_id)

        for access in item.accesses:
            if type(access) == UserAccess:
                if access.get_email() == email:
                    item.accesses.remove(access)
                    break

    def add_department_access_for_file(self, user_mail: str, item_id: UUID, new_access: BaseAccess):
        item = self.getUserFileById(user_mail, item_id)
        item.add_access(new_access)

    def remove_department_access_for_file(self, user_mail: str, item_id: UUID, department: str):
        item = self.getUserFileById(user_mail, item_id)

        for access in item.accesses:
            if type(access) == DepartmentAccess:
                if access.get_department_name() == department:
                    item.accesses.remove(access)
                    break

    def get_accesses_for_item(self, user_mail: str, item_id: UUID) -> list[BaseAccess]:
        item = self.getUserFileById(user_mail, item_id)
        return item.accesses

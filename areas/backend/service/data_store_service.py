from typing import Optional, BinaryIO
import uuid
from copy import deepcopy
from uuid import UUID

from app_states_for_test import ScopeTypeEnum
from core.accesses import BaseAccess, DepartmentAccess, UserAccess, UrlAccess
from core.base_storage_item import BaseStorageItem
from core.directory import Directory
from core.directory_manager import DirectoryManager
from core.files import FileManager, File
from core.space_manager import SpaceManager
from core.user_cloud_space import UserCloudSpace
from decorators.token_required import get_user_by_token
from exceptions.exceptions import ItemNotFoundError, AlreadyExistsError
from repository.data_store_storage_repository import DataStoreStorageRepository
from accessify import private
import logging


class DataStoreService:
    def __init__(self, server_state):
        self.server_state = server_state
        self.data_store_storage_repo = DataStoreStorageRepository(server_state)
        self.scope = ScopeTypeEnum.Prod

    def set_scope(self, scope: ScopeTypeEnum):
        self.scope = scope
        self.data_store_storage_repo.set_scope(scope)

    def search_in_cloud(self, user_mail: str, query: str) -> list[tuple[BaseStorageItem, str]]:
        """
        @param user_mail: user email
        @param query: query
        """
        space_manager: SpaceManager = self.data_store_storage_repo.get_root_dir_by_user_mail(user_mail)
        founded_items: list[tuple[BaseStorageItem, str]] = self.search_in_spaces(space_manager, query)
        return founded_items

    def get_spaces(self, user_mail: str) -> list[UserCloudSpace]:
        return self.data_store_storage_repo.get_user_spaces(user_mail)

    def get_space_content(self, user_mail: str, space_id: UUID) -> list[BaseStorageItem]:
        space: UserCloudSpace = self.data_store_storage_repo.get_user_space_content(user_mail, space_id)

        if space is None:
            raise ItemNotFoundError

        items: list[BaseStorageItem] = []
        items.extend(space.get_directory_manager().items)
        items.extend(space.get_directory_manager().file_manager.items)

        return items

    def get_dir_content(self, user_mail: str, space_id: UUID, dir_id: UUID) -> list[BaseStorageItem]:
        space = self.data_store_storage_repo.get_user_space_content(user_mail, space_id)

        if space is None:
            raise ItemNotFoundError

        directory = self.get_user_dir_in_space(space, dir_id)

        if directory is None:
            raise ItemNotFoundError

        items: list[BaseStorageItem] = []
        items.extend(directory.get_directory_manager().items)
        items.extend(directory.get_directory_manager().file_manager.items)

        return items

    def get_user_dir_in_space(self, space: UserCloudSpace, dir_id: UUID) -> Optional[Directory]:
        for directory in space.get_directory_manager().items:
            if directory.id == dir_id:
                return directory
            else:
                possible_dir = self.get_user_dir_in_another_dir(directory, dir_id)
                if possible_dir is not None:
                    return possible_dir

        return None

    def get_user_dir_in_another_dir(self, directory: Directory, dir_id: UUID) -> Optional[Directory]:
        for directory in directory.get_directory_manager().items:
            if directory.id == dir_id:
                return directory
            else:
                possible_dir = self.get_user_dir_in_another_dir(directory, dir_id)
                if possible_dir is not None:
                    return possible_dir

        return None

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
                    directory=directory_,
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

    def get_item_in_directory_by_id(self, directory: Directory, id_: UUID, recursive=True) -> Optional[BaseStorageItem]:
        if str(directory.id) == str(id_):
            return directory

        directory_manager = directory.directory_manager

        for directory_ in directory_manager.items:
            if str(directory_.id) == str(id_):
                return directory_

            if recursive:
                item = self.get_item_in_directory_by_id(directory=directory_, id_=id_, recursive=recursive)
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
            if str(file.id) == str(id_):
                return file
        return None

    def add_new_file(self, user_email: str, space_id: uuid.UUID, dir_id: uuid.UUID, new_file_name: str, new_file_type: str, new_file_data: str) -> UUID:
        if not (self.is_user_file(user_email, dir_id)):
            raise ItemNotFoundError

        dir_content = self.get_dir_content(user_email, space_id, dir_id)
        for _item in dir_content:
            if _item.name == new_file_name:
                raise AlreadyExistsError
        new_file = File(new_file_name, new_file_type)
        return self.data_store_storage_repo.add_new_file(user_email, space_id, dir_id, new_file, new_file_data)

    def get_user_file_by_id(self, user_mail: str, item_id: UUID) -> Optional[BaseStorageItem]:
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

    def is_user_file(self, user_mail: str, item_id: UUID) -> bool:
        return self.get_user_file_by_id(user_mail, item_id) is not None

    def set_url_access_for_file(self, user_mail: str, item_id, new_access: BaseAccess):
        item = self.get_user_file_by_id(user_mail, item_id)

        if item is None:
            raise ItemNotFoundError

        for access in item.accesses:
            if type(access) == UrlAccess:
                raise AlreadyExistsError

        item.add_access(new_access)
        self.data_store_storage_repo.update_item_access(item)

    def remove_url_access_for_file(self, user_mail: str, item_id: UUID):
        item = self.get_user_file_by_id(user_mail, item_id)

        if item is None:
            raise ItemNotFoundError

        for access in item.accesses:
            if type(access) == UrlAccess:
                item.accesses.remove(access)
                self.data_store_storage_repo.update_item_access(item)
                break

    def add_email_access_for_file(self, user_mail: str, item_id: UUID, new_access: BaseAccess):
        item = self.get_user_file_by_id(user_mail, item_id)

        if item is None:
            raise ItemNotFoundError

        item.add_access(new_access)
        self.data_store_storage_repo.update_item_access(item)
        self.data_store_storage_repo.add_shared_scope(item, new_access)

    def remove_email_access_for_file(self, user_mail: str, item_id: UUID, email: str):
        item = self.get_user_file_by_id(user_mail, item_id)

        if item is None:
            raise ItemNotFoundError

        for access in item.accesses:
            if type(access) == UserAccess:
                if access.get_email() == email:
                    item.accesses.remove(access)
                    self.data_store_storage_repo.update_item_access(item)
                    break

    def add_department_access_for_file(self, user_mail: str, item_id: UUID, new_access: BaseAccess):
        item = self.get_user_file_by_id(user_mail, item_id)

        if item is None:
            raise ItemNotFoundError

        item.add_access(new_access)
        self.data_store_storage_repo.update_item_access(item)

    def remove_department_access_for_file(self, user_mail: str, item_id: UUID, department: str):
        item = self.get_user_file_by_id(user_mail, item_id)

        if item is None:
            raise ItemNotFoundError

        for access in item.accesses:
            if type(access) == DepartmentAccess:
                if access.get_department_name() == department:
                    item.accesses.remove(access)
                    self.data_store_storage_repo.update_item_access(item)
                    break

    def get_accesses_for_item(self, user_mail: str, item_id: UUID) -> list[BaseAccess]:
        item = self.get_user_file_by_id(user_mail, item_id)

        if item is None:
            raise ItemNotFoundError

        return item.accesses

    def rename_item_by_id(self, user_mail: str, item_id: UUID, new_name: str):
        item = self.get_user_file_by_id(user_mail, item_id)
        if item is not None:
            item.name = new_name
            self.data_store_storage_repo.edit_item_name(item)
            return item.name
        else:
            return None

    def move_item(self, user_mail: str, item_id: UUID, target_directory_id: UUID):
        item = self.get_user_file_by_id(user_mail, item_id)
        if item is not None:
            target_directory = self.get_user_file_by_id(user_mail, target_directory_id)
            if target_directory is not None and isinstance(target_directory, Directory):
                source_directory_manager = self.get_parent_directory_manager_by_item_id(user_mail, item_id)
                if isinstance(item, Directory):
                    source_directory_manager.remove_dir(item.name)
                    target_directory.directory_manager.add_items([item])
                elif isinstance(item, File):
                    source_directory_manager.file_manager.remove_item(item)
                    target_directory.directory_manager.file_manager.add_item(item)
                return target_directory.name
        else:
            return None

    @private
    def get_parent_directory_manager_by_item_id(self, user_mail: str, item_id: UUID) -> Optional[DirectoryManager]:
        space_manager: SpaceManager = self.data_store_storage_repo.get_root_dir_by_user_mail(user_mail)

        for space in space_manager.get_spaces():
            file = self.get_file_in_directory_by_id(
                file_manager=space.get_directory_manager().file_manager,
                id_=item_id
            )
            if file is not None:
                return space.get_directory_manager()

            directories_for_search = space.get_directory_manager().items

            while len(directories_for_search):
                directory = directories_for_search.pop(0)
                item = self.get_item_in_directory_by_id(directory=directory, id_=item_id, recursive=False)
                if item is not None:
                    return directory.get_directory_manager()
                else:
                    directories_for_search.extend(directory.directory_manager.items)
        return None

    def download_item(self, user_mail: str, item_id: UUID) -> [Optional[BinaryIO], File]:
        item = self.get_user_file_by_id(user_mail, item_id)
        if item is not None:
            result = self.data_store_storage_repo.get_file_by_item_id(item.id)
            # Пока оставил так, вроде норм, потом мб надо будет поправить
            return [result, item]
        else:
            return [None, None]

    def delete_item(self, user_mail: str, item_id: UUID) -> bool:
        item = self.get_user_file_by_id(user_mail, item_id)
        if item is not None:
            my_directory_manager = self.get_parent_directory_manager_by_item_id(user_mail, item_id)
            if my_directory_manager is not None:
                if isinstance(item, File):
                    my_directory_manager.file_manager.remove_item(item)
                    self.data_store_storage_repo.delete_item_from_db(item)
                    return True
                elif isinstance(item, Directory):
                    my_directory_manager.remove_dir(item.name)
                    self.data_store_storage_repo.delete_item_from_db(item)
                    return True
                else:
                    return False
            else:
                return False

        else:
            return False

    def copy_item(self, user_mail: str, item_id: UUID, target_directory_id: UUID):
        item = self.get_user_file_by_id(user_mail, item_id)
        if item is not None:
            target_directory = self.get_user_file_by_id(user_mail, target_directory_id)
            if target_directory is not None and isinstance(target_directory, Directory):
                if isinstance(item, Directory):
                    new_directory = deepcopy(item)
                    self.copy_directory(directory=new_directory)
                    target_directory.directory_manager.add_items([new_directory])
                elif isinstance(item, File):
                    new_item = deepcopy(item)
                    new_item.id = self.data_store_storage_repo.copy_file(item)
                    target_directory.directory_manager.file_manager.add_item(new_item)
                return target_directory.name
        return None

    def copy_directory(self, directory: Directory):
        directory.id = uuid.uuid4()
        for file in directory.directory_manager.file_manager.items:
            _id = self.data_store_storage_repo.copy_file(file)
            file.id = _id
        for subdirectory in directory.directory_manager.items:
            self.copy_directory(subdirectory)

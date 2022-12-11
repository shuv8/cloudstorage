import base64
import os
import shutil
import uuid
from io import BytesIO
from typing import BinaryIO, Optional

from flask import current_app
from minio import Minio
from sqlalchemy import delete
from sqlalchemy import update

from app_db import get_current_db
from config import *
from core.accesses import BaseAccess, UrlAccess, AccessType, DepartmentAccess, UserAccess
from core.base_storage_item import BaseStorageItem
from core.directory import Directory
from core.files import File
from core.space_manager import SpaceManager
from core.user_cloud_space import UserCloudSpace, SpaceType
from database.database import FileModel, UserModel, UserSpaceModel, DirectoryModel, AccessModel, FileDirectory, \
    DepartmentModel, UrlSpaceModel
from exceptions.exceptions import UserNotFoundError, DepartmentNotFoundError
import shutil


class DataStoreStorageRepository:
    def __init__(self):
        self.db = get_current_db(current_app)
        self.minio_client = DataStoreStorageRepository.get_minio_client()

    @staticmethod
    def get_minio_client():
        client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
        )

        found = client.bucket_exists("cloudstorage")
        if not found:
            client.make_bucket("cloudstorage")
        else:
            pass

        return client

    def get_user_spaces(self, user_mail: str) -> list[UserCloudSpace]:
        return self.get_root_dir_by_user_mail(user_mail).get_spaces()

    def get_user_space_content(self, user_mail: str, space_id: uuid.UUID) -> Optional[UserCloudSpace]:
        spaces: list[UserCloudSpace] = self.get_user_spaces(user_mail)
        for space in spaces:
            if space.get_id() == space_id:
                return space

    def save_file_to_cloud(self, file_name):
        self.minio_client.fput_object("cloudstorage", file_name, f"cache/{file_name}")
        print(f"'cache/{file_name}' is successfully uploaded as object 'test_file.py' to bucket 'cloud_storage'.")
        os.remove(f"cache/{file_name}")

    def get_file_from_cloud(self, file_name):
        try:
            cloud_file_request = self.minio_client.get_object("cloudstorage", file_name)
            return cloud_file_request.data
        except:
            raise FileNotFoundError

    def get_dir_from_cloud(self, dir, zip_name=None, begin_dir_id=None):
        if zip_name is None:
            zip_name = dir.name
            begin_dir_id = dir.id
        os.mkdir(f"cache/{zip_name}")
        for file in dir.directory_manager.file_manager.items:
            file_name = f'{file.id}{file.get_type()}'
            with open(f'cache/{zip_name}/{file_name}', "wb") as fh:
                fh.write(self.get_file_from_cloud(file_name))
        for directory in dir.directory_manager.items:
            zip_name_dir = f"{zip_name}/{directory.name}"
            self.get_dir_from_cloud(directory, zip_name=zip_name_dir, begin_dir_id=begin_dir_id)
        if dir.id == begin_dir_id:
            zip_file = shutil.make_archive(format='zip', root_dir="cache/", base_dir=f'{zip_name}',
                                           base_name=f"cache/{zip_name}")
            shutil.rmtree(f"cache/{zip_name}")
            return zip_file
        else:
            return None

    def remove_files_from_cloud(self, file_name):
        self.minio_client.remove_object("cloudstorage", file_name)

    def add_new_file(self, dir_id: uuid.UUID, new_file: File,
                     new_file_data: str) -> uuid.UUID:

        directory: DirectoryModel = DirectoryModel.query.filter_by(id=str(dir_id)).first()

        file = FileModel(
            id=str(new_file.id),
            name=new_file.name,
            type=new_file.type,
        )

        self.db.session.add(file)
        directory.files.append(file)

        self.db.session.commit()

        file_name = f'{new_file.id}{new_file.get_type()}'
        with open(f'cache/{file_name}', "wb") as fh:
            fh.write(base64.decodebytes(str.encode(new_file_data)))

        self.save_file_to_cloud(file_name)
        return new_file.id

    def get_binary_file_by_id(self, file_id: uuid.UUID, file_type: str) -> BinaryIO:
        return BytesIO(self.get_file_from_cloud(f"{file_id}{file_type}"))

    def get_binary_dir_by_id(self, dir: Directory) -> BinaryIO:
        zip_file = self.get_dir_from_cloud(dir)
        with open(f'{zip_file}', 'rb') as fz:
            data = fz.read()
        os.remove(f'{zip_file}')
        return BytesIO(data)

    def add_new_directory(self, new_directory: Directory, parent_id: uuid.UUID) -> uuid.UUID:
        new_directory_model = DirectoryModel(
            id=str(new_directory.get_id()),
            name=new_directory.get_name(),
        )

        parent_directory = DirectoryModel.query.filter_by(id=str(parent_id)).first()
        parent_directory.inner_directories.append(new_directory_model)

        self.db.session.commit()

        return new_directory.get_id()

    def fill_directory_with_data(self, directory: DirectoryModel) -> Directory:
        partly_root_directory = Directory(
            _id=uuid.UUID(directory.id),
            name=directory.name,
        )

        accesses: list[BaseAccess] = []
        for access in directory.accesses:
            if access.access_type == AccessType.Url:
                accesses.append(
                    UrlAccess(
                        url=access.value,
                        access_type=access.access_level
                    )
                )
            if access.access_type == AccessType.User:
                accesses.append(
                    UserAccess(
                        email=access.value,
                        access_type=access.access_level
                    )
                )
            if access.access_type == AccessType.Department:
                accesses.append(
                    DepartmentAccess(
                        department_name=access.value,
                        access_type=access.access_level
                    )
                )
        partly_root_directory.accesses = accesses

        files_in_directory: list[File] = []
        for file in directory.files:

            accesses: list[BaseAccess] = []
            for access in file.accesses:
                if access.access_type == AccessType.Url:
                    accesses.append(
                        UrlAccess(
                            url=access.value,
                            access_type=access.access_level
                        )
                    )
                if access.access_type == AccessType.User:
                    accesses.append(
                        UserAccess(
                            email=access.value,
                            access_type=access.access_level
                        )
                    )
                if access.access_type == AccessType.Department:
                    accesses.append(
                        DepartmentAccess(
                            department_name=access.value,
                            access_type=access.access_level
                        )
                    )

            files_in_directory.append(
                File(
                    name=file.name,
                    _id=file.id,
                    _type=file.type,
                    accesses=accesses
                )
            )

        inner_directories: list[Directory] = []
        for inner_directory in directory.inner_directories:
            inner_directories.append(self.fill_directory_with_data(inner_directory))

        partly_root_directory.get_directory_manager().items = inner_directories
        partly_root_directory.get_directory_manager().file_manager.items = files_in_directory

        return partly_root_directory

    def get_root_dir_by_user_mail(self, user_mail: str) -> SpaceManager:
        user: UserModel = UserModel.query.filter_by(email=user_mail).first()
        user_space_models: list[UserSpaceModel] = UserSpaceModel.query.filter_by(user_id=user.id).all()

        spaces: list[UserCloudSpace] = list()
        for space_model in user_space_models:
            user_cloud = UserCloudSpace(
                _id=uuid.UUID(space_model.id),
                space_type=space_model.space_type
            )

            directory: DirectoryModel = DirectoryModel.query.filter_by(id=space_model.root_directory.id).first()

            root_directory = self.fill_directory_with_data(directory)

            user_cloud.get_directory_manager().items = [root_directory]

            spaces.append(
                user_cloud
            )

        space_manager = SpaceManager(
            spaces=spaces
        )

        return space_manager

    def copy_file(self, file, directory_id):
        new_id = uuid.uuid4()
        old_file_model: FileModel = FileModel.query.filter_by(id=str(file.id)).first()
        old_file_dir_model: FileDirectory = FileDirectory.query.filter_by(file_id=str(file.id)).first()
        new_file_model = FileModel(
            id=str(new_id),
            name=old_file_model.name + '_copy' if old_file_dir_model.directory_id == str(
                directory_id) else old_file_model.name,
            type=old_file_model.type
        )
        new_file_dir_model = FileDirectory(
            file_id=str(new_id),
            directory_id=str(directory_id)
        )

        file_name = f'{old_file_model.id}{old_file_model.type}'
        new_file_name = f'{str(new_id)}{old_file_model.type}'
        file_data = self.get_binary_file_by_id(old_file_model.id, old_file_model.type)

        with open(f'cache/{file_name}', "wb") as fh:
            fh.write(BytesIO(file_data.read()).getbuffer())
        src = f'cache/{file_name}'
        dst = f'cache/{new_file_name}'
        shutil.copyfile(src, dst)

        self.save_file_to_cloud(new_file_name)
        os.remove(src)

        self.db.session.add(new_file_model)
        self.db.session.add(new_file_dir_model)
        self.db.session.commit()
        return new_id

    def copy_directory(self, directory, target_directory_id):
        new_id = uuid.uuid4()
        old_directory_model: DirectoryModel = DirectoryModel.query.filter_by(id=str(directory.id)).first()
        new_directory_model = DirectoryModel(
            id=str(new_id),
            name=old_directory_model.name + '_copy' if old_directory_model.parent_id == str(
                target_directory_id) else old_directory_model.name,
            is_root=False,
            parent_id=str(target_directory_id)
        )
        self.db.session.add(new_directory_model)
        self.db.session.commit()
        return new_id

    def edit_item_name(self, item):
        if isinstance(item, File):
            self.db.session.execute(update(FileModel).where(FileModel.id == str(item.id)).values(name=item.name))
        elif isinstance(item, Directory):
            self.db.session.execute(
                update(DirectoryModel).where(DirectoryModel.id == str(item.id)).values(name=item.name))
        self.db.session.commit()

    def remove_shared_space_by_email(self, item: BaseStorageItem, email: str):
        user: UserModel = UserModel.query.filter_by(email=email).first()

        if user is None:
            raise UserNotFoundError

        if isinstance(item, File):
            for space in user.spaces:
                if space.space_type == SpaceType.Shared:
                    if space.root_directory.files[0].id == str(item.id):
                        user.spaces.remove(space)
                        if space is not None:
                            self.db.session.execute(delete(UserSpaceModel).where(UserSpaceModel.id == space.id))
        elif isinstance(item, Directory):
            for space in user.spaces:
                if space.space_type == SpaceType.Shared:
                    if space.root_directory.id == str(item.id):
                        user.spaces.remove(space)
                        if space is not None:
                            self.db.session.execute(delete(UserSpaceModel).where(UserSpaceModel.id == space.id))
        self.db.session.commit()

    def remove_shared_space_by_url(self, item: BaseStorageItem):
        url_spaces: list[UrlSpaceModel] = UrlSpaceModel.query.all()

        if isinstance(item, File):
            for space in url_spaces:
                if space.root_directory.files[0].id == str(item.id):
                    url_spaces.remove(space)
                    if space is not None:
                        self.db.session.execute(delete(UrlSpaceModel).where(UrlSpaceModel.id == space.id))
        elif isinstance(item, Directory):
            for space in url_spaces:
                if space.root_directory.id == str(item.id):
                    url_spaces.remove(space)
                    if space is not None:
                        self.db.session.execute(delete(UrlSpaceModel).where(UrlSpaceModel.id == space.id))
        self.db.session.commit()

    def remove_shared_space_by_department(self, item: BaseStorageItem, department_name: str):
        department: DepartmentModel = DepartmentModel.query.filter_by(name=department_name).first()

        if department is None:
            raise DepartmentNotFoundError

        for user in department.users:
            self.remove_shared_space_by_email(item, user.email)

    def add_shared_space_for_file_model_by_email(self, item: FileModel, email: str):
        user: UserModel = UserModel.query.filter_by(email=email).first()

        new_space = UserSpaceModel(
            id=str(uuid.uuid4().hex),
            space_type=SpaceType.Shared,
        )
        self.db.session.add(new_space)

        file: FileModel = FileModel.query.filter_by(id=item.id).first()
        directory = DirectoryModel(
            id=str(uuid.uuid4().hex),
            name="Root",
            is_root=True,
        )
        self.db.session.add(directory)
        new_space.root_directory = directory
        new_space.root_directory.files = [file]

        user.spaces.append(new_space)

    def add_shared_space_for_directory_model_by_email(self, item: DirectoryModel, email: str):
        user: UserModel = UserModel.query.filter_by(email=email).first()

        new_space = UserSpaceModel(
            id=str(uuid.uuid4().hex),
            space_type=SpaceType.Shared,
        )
        self.db.session.add(new_space)

        directory: DirectoryModel = DirectoryModel.query.filter_by(id=item.id).first()
        new_space.root_directory = directory

        user.spaces.append(new_space)

    def add_shared_space_by_email(self, item: BaseStorageItem, email: str):
        user: UserModel = UserModel.query.filter_by(email=email).first()

        if user is None:
            raise UserNotFoundError

        new_space = UserSpaceModel(
            id=str(uuid.uuid4()),
            space_type=SpaceType.Shared,
        )
        self.db.session.add(new_space)

        if isinstance(item, File):
            file: FileModel = FileModel.query.filter_by(id=str(item.id)).first()
            directory = DirectoryModel(
                id=str(uuid.uuid4()),
                name="Root",
                is_root=True,
            )
            self.db.session.add(directory)
            new_space.root_directory = directory
            new_space.root_directory.files = [file]
        elif isinstance(item, Directory):
            directory: DirectoryModel = DirectoryModel.query.filter_by(id=str(item.id)).first()
            new_space.root_directory = directory

        user.spaces.append(new_space)

    def add_shared_space_by_type(self, item: BaseStorageItem, access: BaseAccess):
        if type(access) is UrlAccess:
            url_space = UrlSpaceModel(
                id=access.get_url()
            )

            if isinstance(item, File):
                file: FileModel = FileModel.query.filter_by(id=str(item.id)).first()
                directory = DirectoryModel(
                    id=str(uuid.uuid4()),
                    name="Root",
                    is_root=True,
                )
                self.db.session.add(directory)
                url_space.root_directory = directory
                url_space.root_directory.files = [file]
            elif isinstance(item, Directory):
                directory: DirectoryModel = DirectoryModel.query.filter_by(id=str(item.id)).first()
                url_space.root_directory = directory

            self.db.session.add(url_space)

        elif type(access) is UserAccess:
            self.add_shared_space_by_email(item, access.get_email())

        elif type(access) is DepartmentAccess:
            department: DepartmentModel = DepartmentModel.query.filter_by(name=access.get_department_name()).first()

            if department is None:
                raise DepartmentNotFoundError

            for user in department.users:
                self.add_shared_space_by_email(item, user.email)

        self.db.session.commit()

    def update_item_access(self, item: BaseStorageItem):
        accesses: list[AccessModel] = []

        for access in item.accesses:
            if type(access) is UrlAccess:
                accesses.append(
                    AccessModel(
                        access_level=access.access_type,
                        access_type=AccessType.Url,
                        value=access.get_url(),
                    )
                )
            elif type(access) is UserAccess:
                accesses.append(
                    AccessModel(
                        access_level=access.access_type,
                        access_type=AccessType.User,
                        value=access.get_email(),
                    )
                )
            elif type(access) is DepartmentAccess:
                accesses.append(
                    AccessModel(
                        access_level=access.access_type,
                        access_type=AccessType.Department,
                        value=access.get_department_name(),
                    )
                )

        if isinstance(item, File):
            file: FileModel = FileModel.query.filter_by(id=str(item.id)).first()
            for access in file.accesses:
                file.accesses.remove(access)
                self.db.session.execute(delete(AccessModel).where(AccessModel.id == access.id))
            file.accesses = accesses
            self.db.session.commit()
        elif isinstance(item, Directory):
            directory: DirectoryModel = DirectoryModel.query.filter_by(id=str(item.id)).first()
            for access in directory.accesses:
                directory.accesses.remove(access)
                self.db.session.execute(delete(AccessModel).where(AccessModel.id == access.id))
            directory.accesses = accesses
            self.db.session.commit()

    def delete_item_from_db(self, item):
        if isinstance(item, File):
            self.db.session.execute(delete(FileModel).where(FileModel.id == str(item.id)))
            self.db.session.execute(delete(FileDirectory).where(FileDirectory.file_id == str(item.id)))
            self.remove_files_from_cloud(f"{item.id}{item.type}")
        elif isinstance(item, Directory):
            self.db.session.execute(
                delete(DirectoryModel).where(DirectoryModel.id == str(item.id)))
        self.db.session.commit()

    def move_item_in_db(self, item, target_directory):
        if isinstance(item, File):
            self.db.session.execute(update(FileDirectory).where(
                FileDirectory.file_id == str(item.id)).values(directory_id=str(target_directory.id)))
        elif isinstance(item, Directory):
            self.db.session.execute(update(DirectoryModel).where(
                DirectoryModel.id == str(item.id)).values(parent_id=str(target_directory.id)))
        self.db.session.commit()

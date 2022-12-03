from typing import BinaryIO, Optional
from uuid import UUID, uuid4

from core.directory import Directory
from core.files import File
from core.space_manager import SpaceManager
from core.user_cloud_space import UserCloudSpace, SpaceType
from core.department_manager import DepartmentManager
from core.department import Department
from core.user_manager import UserManager
from core.user import User
from exceptions.exceptions import ItemNotFoundError


class DataBaseTemporary:

    def __init__(self):
        self.user_cloud_space_1_ = UserCloudSpace(
            _id=uuid4(),
            space_type=SpaceType.Regular
        )

        self.user_cloud_space_2_ = UserCloudSpace(
            _id=UUID(hex='abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1'),
            space_type=SpaceType.Shared
        )

        self.space_manager_ = SpaceManager(
            spaces=[self.user_cloud_space_1_, self.user_cloud_space_2_]
        )

        self.user_1_ = User(
            email="test_mail@mail.com",
            password="$2b$12$ikBnpSAHmRPfgOAh9HvQ/.KNLk/mAV5rGH7xRMcVmh9ozrjApsYIC",
            username="username",
            space_manager=self.space_manager_
        )

        self.user_2_ = User(
            email="test2_mail@mail.com",
            password="$2b$12$ikBnpSAHmRPfgOAh9HvQ/.KNLk/mAV5rGH7xRMcVmh9ozrjApsYIC",
            username="username",
        )

        self.user_cloud_space_1_.get_directory_manager().items = [
            Directory(name="wow", _id=UUID(hex='abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1')),
            Directory(name='second', _id=UUID(hex='4c3b76d1-fe24-4fdf-afdf-7c38adbdab14')),
            Directory(name='delete', _id=UUID(hex='4c3b76d1-fe24-4fdf-afdf-7c38adbdab15')),
        ]

        self.user_cloud_space_1_.get_directory_manager().file_manager.items = [
            File(name="wow3", _type=".type",
                 _id=UUID(hex='abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')),
            File(name="test6", _type=".e"),
            File(name="image", _type=".png",
                 _id=UUID(hex='abd9cd7f-9ffd-41b0-bce4-eb14b51a6d71')),
            File(name="test", _type=".txt",
                 _id=UUID(hex='abd9cd7f-9ffd-41b0-bce4-eb14b51a6d72')),
            File(name="test2", _type=".txt",
                 _id=UUID(hex='abd9cd7f-9ffd-41b0-d1e4-eb14b51a6d72')),
            File(name="test3", _type=".txt",
                 _id=UUID(hex='abd9cd7d-9ffd-41b0-d1e4-eb14b51a6d72')),
        ]

        self.user_cloud_space_2_.get_directory_manager().items = [
            Directory(name="test1", _id=UUID(hex='abd9cd7f-9ffd-42b0-bce4-eb14b51a1fa4'))
        ]

        self.user_cloud_space_2_.get_directory_manager().file_manager.items = [
            File(name="test2", _type=".ty"),
        ]

        self.user_cloud_space_2_.get_directory_manager().items[0].get_directory_manager().file_manager.items = [
            File(name="test42", _type=".ty"),
        ]

        self.user_cloud_space_2_.get_directory_manager().items[0].get_directory_manager().items = [
            Directory(name="test4242", _id=UUID(hex='abd9cd7f-9ffd-42b0-bce4-eb14b51a1fa5'))
        ]

        self.users = {
            "bb01bafc-21f1-4af8-89f9-79aa0de840c8": self.user_1_,
            "5786c9ba-776f-4d53-804b-e5f87a01ec1f": self.user_2_,
            self.user_1_.email: self.user_1_,
            self.user_2_.email: self.user_2_
        }

        self.user_manager = UserManager([self.user_1_, self.user_2_])

        department_1 = Department('Test_department_1', [self.user_1_, self.user_2_])
        department_2 = Department('Test_department_2', None)

        self.departments = {
            "Test_department_1": department_1,
            "Test_department_2": department_2
        }

        self.department_manager = DepartmentManager([department_1, department_2])

    def get_user_manager(self):
        return self.user_manager

    def get_department_list(self):
        return self.department_manager.get_departments()

    def get_department_by_name(self, department_name):
        self.department_manager.get_department(department_name)

    def add_new_department(self, new_department: Department):
        self.department_manager.add_department(new_department)
        self.departments[new_department.department_name] = new_department

    def delete_department_by_name(self, department_name: str):
        self.department_manager.remove_department_by_department_name(department_name)

    def get_space_manager_by_user_mail(self, mail: str) -> SpaceManager:
        return self.users[mail].space_manager

    def get_spaces_by_user_mail(self, mail: str) -> list[UserCloudSpace]:
        return self.get_space_manager_by_user_mail(mail).get_spaces()

    def get_space_content_by_user_mail(self, mail: str, space_id: UUID) -> UserCloudSpace:
        spaces = self.get_spaces_by_user_mail(mail)
        for space in spaces:
            if space.get_id() == space_id:
                return space

    def add_new_user(self, new_user: User):
        self.user_manager.add_user(new_user)
        self.users[new_user.get_id()] = new_user

    def get_user(self, id: UUID):
        return self.user_manager.get_user(id)

    def get_user_by_email(self, email: str):
        return self.user_manager.get_user_by_email(email)

    def add_new_file(self, user_email: str, space_id: UUID, dir_id: UUID, file: File) -> UUID:
        user = self.user_manager.get_user_by_email(user_email)
        spaces = user.get_space_manager().get_spaces()
        for _space in spaces:
            if _space.get_id() == space_id:
                current_space = _space
                break
        for _dir in current_space.get_directory_manager().get_items():
            if _dir.get_id() == dir_id:
                current_dir = _dir
                break
        current_dir.get_directory_manager().get_file_manager().add_item(file)
        return file.get_id()
        

    @staticmethod
    def get_file_by_item_id(item_id: UUID) -> BinaryIO:
        _file = BinaryIO()
        return _file

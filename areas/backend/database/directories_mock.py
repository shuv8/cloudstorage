import uuid

from core.directory import Directory
from core.files import File
from core.space_manager import SpaceManager
from core.user import User
from core.user_cloud_space import UserCloudSpace, SpaceType


class DataBaseTemporaryMock:
    user_cloud_space_1_ = UserCloudSpace(
        _id=uuid.uuid4(),
        space_type=SpaceType.Regular
    )

    user_cloud_space_2_ = UserCloudSpace(
        _id=uuid.uuid4(),
        space_type=SpaceType.Shared
    )

    space_manager_ = SpaceManager(
        spaces=[user_cloud_space_1_, user_cloud_space_2_]
    )

    user_1_ = User(
        email="test_mail@mail.com",
        password="password",
        username="username",
        space_manager=space_manager_
    )

    user_2_ = User(
        email="test2_mail@mail.com",
        password="password",
        username="username",
    )

    user_cloud_space_1_.get_directory_manager().items = [
        Directory(name="wow", _id='abd9cd7f-9ffd-42b0-bce4-eb14b51n1jn1'),
        Directory(name='second', _id='xyz9cd7f-9ffd-42b0-bce4-eb14b51n1jn1')
    ]

    user_cloud_space_1_.get_directory_manager().file_manager.items = [
        File(name="wow3", _type=".type", _id='abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73'),
        File(name="test6", _type=".e"),
        File(name="image", _type=".png", _id='abd9cd7f-9ffd-41b0-bce4-eb14b51a6d71'),
        File(name="test", _type=".txt", _id='abd9cd7f-9ffd-41b0-bce4-eb14b51a6d72'),
    ]

    user_cloud_space_2_.get_directory_manager().items = [
        Directory(name="test1")
    ]

    users = {
        "test_mail@mail.com": user_1_,
        "test2_mail@mail.com": user_2_
    }

    def get_space_by_user_mail(self, mail: str) -> SpaceManager:
        return self.users[mail].space_manager

import pytest

from core.accesses import UserAccess
from core.department import Department
from core.department_manager import DepartmentManager
from core.files import File
from core.role import Role
from core.user import User
from core.user_cloud_space import UserCloudSpace, SpaceType
from core.user_manager import UserManager


@pytest.fixture()
def user():
    return User(
        email="test_mail@mail.com",
        password="password",
        username="username",
    )


@pytest.fixture()
def admin():
    return User(
        email="test_mail2@mail.com",
        password="password",
        username="username",
        role=Role.Admin
    )


@pytest.fixture()
def user_manager():
    return UserManager(users=None)


@pytest.fixture()
def department(user):
    return Department(
        department_name="test",
        users=None
    )


@pytest.fixture()
def department_manager():
    return DepartmentManager(
        departments=None
    )


@pytest.fixture()
def file():
    return File(
        name="test",
        _type=".txt",
    )


@pytest.fixture()
def user_access(admin):
    return UserAccess(admin.email)


class TestUserScenario:
    def test_main(
            self,
            user,
            admin,
            user_manager,
            department,
            department_manager,
            file,
            user_access
    ):
        # Let's create first Users

        user_manager.add_user(user)
        user_manager.add_user(admin)

        # Let's create a new department manager

        user.department_manager = department_manager
        admin.department_manager = department_manager

        # Let's create anew department

        department_manager.add_department(department)

        # Let's add the user to the department

        department_manager.add_users_to_department([user, admin], department.department_name)

        # ---- Now, let's check, that everything is OK

        assert user_manager.users[0].department_manager.get_users_list_by_department_name(
            department.department_name) == [user, admin]
        assert user_manager.users[1].department_manager.get_users_list_by_department_name(
            department.department_name) == [user, admin]

        # ---- Let's check if our users have real directories

        user_: User = user_manager.users[0]
        default_space: UserCloudSpace = user_.space_manager.get_spaces()[0]
        assert default_space.get_space_type() == SpaceType.Regular
        assert default_space.get_directory_manager().items == []

        user_2: User = user_manager.users[1]
        default_space_2: UserCloudSpace = user_2.space_manager.get_spaces()[0]
        assert default_space_2.get_directory_manager().items == []

        # ---- Let's try to create something

        user_.space_manager.get_spaces()[0].get_directory_manager().create_dir("My lovely folder")
        user_.space_manager.get_spaces()[0].get_directory_manager().create_dir("My lovely folder 2")

        user_.space_manager.get_spaces()[0].get_directory_manager().file_manager.add_item(file)

        # And something more complicated..

        user_.space_manager.get_spaces()[0].get_directory_manager().get_dir(
            "My lovely folder").directory_manager.create_dir("NEXT LEVEL")
        user_.space_manager.get_spaces()[0].get_directory_manager().get_dir(
            "My lovely folder").directory_manager.file_manager.add_item(file)

        # Let's check correctness

        main_directory = user_.space_manager.get_spaces()[0].get_directory_manager()

        assert len(main_directory.items) == 2
        assert len(main_directory.file_manager.items) == 1

        sub_directory = main_directory.get_dir("My lovely folder").directory_manager

        assert len(sub_directory.items) == 1
        assert len(sub_directory.file_manager.items) == 1

        # By the way, what about accesses

        main_directory.get_dir("My lovely folder").add_access(user_access)

        user_access: UserAccess = main_directory.get_dir("My lovely folder").accesses[0]
        assert user_access.get_email() == admin.email

import pytest

from core.user_cloud_space import SpaceType
from tests.test_cc.conftest_constants import *
from web_server import create_app
from bcrypt import gensalt, hashpw

app_testing = create_app(True, 'sqlite:///:memory:')


@pytest.fixture(scope='function')
def user_space():
    from app_db import get_current_db
    with app_testing.app_context():
        db_ = get_current_db(app_testing)
        from database.database import DirectoryModel, UserSpaceModel, FileModel, UrlSpaceModel

        test_dir = DirectoryModel(
            id=root_dir_1_id,
            name="Root",
            is_root=True,
        )

        test_file = FileModel(
            id=file_1_id,
            name="file_for",
            type=".vasya",
        )

        test_dir_2 = DirectoryModel(
            id=dir_2_id,
            name="Bla",
        )

        test_dir_3 = DirectoryModel(
            id=dir_3_id,
            name="Bla",
        )

        test_file_2 = FileModel(
            id=file_2_id,
            name="test_file_for",
            type=".test",
        )

        test_file_3 = FileModel(
            id=file_3_id,
            name="test1",
            type=".txt",
        )

        test_file_4 = FileModel(
            id=file_4_id,
            name="test2",
            type=".txt",
        )

        db_.session.add(test_file)
        db_.session.add(test_file_2)
        db_.session.add(test_file_3)
        db_.session.add(test_file_4)

        test_dir_2.files.append(test_file_2)
        test_dir_2.files.append(test_file_3)
        test_dir_2.files.append(test_file_4)
        test_dir.files.append(test_file)
        test_dir.inner_directories.append(test_dir_2)
        test_dir.inner_directories.append(test_dir_3)
        db_.session.add(test_dir)

        url_space = UrlSpaceModel(
            id=url_space_1_id,
            root_directory_id=root_dir_1_id
        )
        db_.session.add(url_space)
        db_.session.commit()

        test_space = UserSpaceModel(
            id=space_1_id,
            space_type=SpaceType.Regular,
        )
        test_space.root_directory = test_dir
        db_.session.add(test_space)

        return test_space


@pytest.fixture(scope='function')
def admin_user():
    from app_db import get_current_db
    with app_testing.app_context():
        db_ = get_current_db(app_testing)
        from database.database import UserModel
        from core.role import Role
        test_user = UserModel(
            id=admin_id,
            email='admin@mail.com',
            username='admin',
            passwordHash=hashpw(str('password').encode(), gensalt()).decode(),
            role=Role.Admin
        )

        db_.session.add(test_user)
        db_.session.commit()
        return test_user


@pytest.fixture(scope='function')
def casual_user_2():
    from app_db import get_current_db
    with app_testing.app_context():
        db_ = get_current_db(app_testing)
        from database.database import UserModel
        from core.role import Role
        test_user = UserModel(
            id=casual_user_2_id,
            email='user2@mail.com',
            username='user 2',
            passwordHash=hashpw(str('password1').encode(), gensalt()).decode(),
            role=Role.Client
        )

        db_.session.add(test_user)
        db_.session.commit()
        return test_user


@pytest.fixture(scope='function')
def casual_user(user_space):
    from app_db import get_current_db
    with app_testing.app_context():
        db_ = get_current_db(app_testing)
        from database.database import UserModel
        from core.role import Role
        test_user = UserModel(
            id=casual_user_id,
            email='user@mail.com',
            username='user',
            passwordHash=hashpw(str('password').encode(), gensalt()).decode(),
            role=Role.Client
        )
        test_user.spaces.append(user_space)

        db_.session.add(test_user)
        db_.session.commit()
        return test_user


@pytest.fixture(scope='function')
def add_departments():
    from app_db import get_current_db
    with app_testing.app_context():
        db_ = get_current_db(app_testing)
        from database.database import DepartmentModel
        test_dep_1 = DepartmentModel(name='Test_department_1')
        test_dep_2 = DepartmentModel(name='Test_department_2')
        db_.session.add_all([test_dep_1, test_dep_2])
        db_.session.commit()
        return [test_dep_1, test_dep_2]


@pytest.fixture(scope='function')
def fill_db(add_departments, admin_user, casual_user, casual_user_2):
    data = {
        'departments': add_departments,
        'admin': admin_user,
        'user': casual_user,
        'user2': casual_user_2,
    }
    return data


@pytest.fixture(scope='function')
def client():
    with app_testing.app_context():
        yield app_testing.test_client()
        app_testing.db.session.remove()
        app_testing.db.drop_all()
        app_testing.db.create_all()


@pytest.fixture
def app_client_admin(client, fill_db):
    login_data = {'email': 'admin@mail.com', 'password': 'password'}
    client.put('/login', json=login_data)
    yield client


@pytest.fixture
def app_client_user(client, fill_db):
    login_data = {'email': 'user@mail.com', 'password': 'password'}
    client.put('/login', json=login_data)
    yield client

import pytest

from core.user_cloud_space import SpaceType
from web_server import create_app
from bcrypt import gensalt, hashpw

app_testing = create_app(True, 'sqlite:///:memory:')


@pytest.fixture
def client():
    with app_testing.app_context():
        yield app_testing.test_client()
        app_testing.db.session.remove()
        app_testing.db.drop_all()
        app_testing.db.create_all()


@pytest.fixture(scope='function')
def admin_user():
    from app_db import get_current_db
    db_ = get_current_db(app_testing)
    from database.users.user_model import UserModel, DirectoryModel, UserSpaceModel, FileModel
    from core.role import Role
    test_user = UserModel(
        id="bb01bafc-21f1-4af8-89f9-79aa0de840c8",
        email='admin@mail.com',
        username='admin',
        passwordHash=hashpw(str('password').encode(), gensalt()).decode(),
        role=Role.Admin
    )

    # Create start directory
    test_file = FileModel(
        id="abd9cd7f-9ffd-41b0-bce4-eb14b51a6d72",
        name="file_for",
        type=".vasya",
    )

    test_file_2 = FileModel(
        id="abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73",
        name="test_file_for",
        type=".test",
    )

    # Create start directory
    test_dir = DirectoryModel(
        id="bb01bafc-21f1-4af8-89f9-79aa0de840c0",
        name="Root",
        is_root=True,
    )

    test_dir_2 = DirectoryModel(
        id="abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1",
        name="Bla",
    )
    db_.session.add(test_file)

    test_dir_2.files.append(test_file_2)
    test_dir.files.append(test_file)
    test_dir.inner_directories.append(test_dir_2)
    db_.session.add(test_dir)

    test_space = UserSpaceModel(
        id="bb01bafc-21f1-4af8-89f9-79aa0de840a2",
        user_id=test_user.id,
        space_type=SpaceType.Regular,
    )
    test_space.root_directory = test_dir

    db_.session.add(test_space)
    db_.session.add(test_user)
    db_.session.commit()
    return test_user


@pytest.fixture(scope='function')
def casual_user():
    from app_db import get_current_db
    db_ = get_current_db(app_testing)
    from database.users.user_model import UserModel
    from core.role import Role
    test_user = UserModel(
        id="bb01bafc-21f1-4af8-89f9-79aa0de840c1",
        email='user@mail.com',
        username='user',
        passwordHash=hashpw(str('password').encode(), gensalt()).decode(),
        role=Role.Client
    )
    db_.session.add(test_user)
    db_.session.commit()
    return test_user


@pytest.fixture(scope='function')
def add_departments():
    from app_db import get_current_db
    db_ = get_current_db(app_testing)
    from database.users.user_model import DepartmentModel
    test_dep_1 = DepartmentModel(name='Test_department_1')
    test_dep_2 = DepartmentModel(name='Test_department_2')
    db_.session.add_all([test_dep_1, test_dep_2])
    db_.session.commit()
    return [test_dep_1, test_dep_2]


@pytest.fixture(scope='function')
def fill_db(add_departments, admin_user, casual_user):
    data = {
        'departments': add_departments,
        'admin': admin_user,
        'user': casual_user
    }
    return data


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

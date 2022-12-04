import pytest
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
    from database.users.user_model import UserModel
    from core.role import Role
    test_user = UserModel(
        id="bb01bafc-21f1-4af8-89f9-79aa0de840c8",
        email='test_mail@mail.com',
        username='test',
        passwordHash=hashpw(str('password').encode(), gensalt()).decode(),
        role=Role.Admin
    )
    db_.session.add(test_user)
    db_.session.commit()


@pytest.fixture
def app_client_admin(client, admin_user):
    login_data = {'email': 'test_mail@mail.com', 'password': 'password'}
    response = client.put('/login', json=login_data)
    yield client


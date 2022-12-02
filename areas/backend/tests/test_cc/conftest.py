import pytest
from web_server import app


@pytest.fixture(scope='function')
def app_client():
    app.testing = True
    test_client = app.test_client()
    login_data = {'email': 'test_mail@mail.com', 'password': 'password'}
    test_client.put('/login', json=login_data)
    return test_client

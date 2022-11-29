import pytest
from web_server import app


@pytest.fixture(scope='function')
def app_client():
    app.testing = True
    return app.test_client()

import pytest

from tests.test_cc.conftest_constants import invalid_token


class TestLogin:

    def test_who(self, app_client_user):
        response = app_client_user.get(f'/whoiam')
        assert response.status_code == 200
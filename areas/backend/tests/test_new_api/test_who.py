import pytest

from core.role import Role
from tests.test_new_api.conftest_constants import casual_user_id, admin_id


class TestWhoIAm:

    def test_who_client(self, app_client_user):
        response = app_client_user.get(f'/whoiam')
        assert response.status_code == 200
        resp_json = response.json
        assert resp_json['id'] == casual_user_id
        assert resp_json['email'] == 'user@mail.com'
        assert resp_json['username'] == 'user'
        assert resp_json['role'] == Role.Client.value

    def test_who_admin(self, app_client_admin):
        response = app_client_admin.get(f'/whoiam')
        assert response.status_code == 200
        resp_json = response.json
        assert resp_json['id'] == admin_id
        assert resp_json['email'] == 'admin@mail.com'
        assert resp_json['username'] == 'admin'
        assert resp_json['role'] == Role.Admin.value

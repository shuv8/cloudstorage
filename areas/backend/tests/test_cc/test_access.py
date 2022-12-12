import pytest

from tests.test_cc.conftest_constants import file_2_id, dir_3_id


class TestAccesses:

    def test_get_access(self, app_client_user):
        response = app_client_user.get(path=f'/accesses/{file_2_id}')
        assert response.status_code == 200

        response = app_client_user.get(path=f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d70')
        assert response.status_code == 401

    def test_set_reset_access_url(self, app_client_user):
        response = app_client_user.put(path=f'/set_access/{file_2_id}?view_only=true')
        assert response.status_code == 200
        response = app_client_user.put(path=f'/set_access/{file_2_id}?view_only=false')
        assert response.status_code == 200
        response = app_client_user.put(path=f'/set_access/{file_2_id}?view_only=false')
        assert response.status_code == 200
        response = app_client_user.get(path=f'/accesses/{file_2_id}')
        assert response.status_code == 200
        response = app_client_user.delete(path=f'/reset_access/{file_2_id}')
        assert response.status_code == 200
        response = app_client_user.delete(path=f'/reset_access/{file_2_id}')
        assert response.status_code == 200
        assert response.json['status'] == "nothing to remove"
        # Let's test we can't modify access for file with unavailable ID
        response = app_client_user.put(path=f'/set_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d70')
        assert response.status_code == 401
        response = app_client_user.delete(path=f'/reset_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d40')
        assert response.status_code == 401

    def test_set_reset_access_url_directory(self, app_client_user):
        response = app_client_user.put(path=f'/set_access/{dir_3_id}?view_only=true')
        assert response.status_code == 200
        response = app_client_user.put(path=f'/set_access/{dir_3_id}?view_only=false')
        assert response.status_code == 200
        response = app_client_user.get(path=f'/accesses/{dir_3_id}')
        assert response.status_code == 200
        response = app_client_user.delete(path=f'/reset_access/{dir_3_id}')
        assert response.status_code == 200
        response = app_client_user.delete(path=f'/reset_access/{dir_3_id}')
        assert response.status_code == 200
        assert response.json['status'] == "nothing to remove"

    def test_set_reset_access_url_2(self, app_client_user):
        response = app_client_user.put(path=f'/set_access/{file_2_id}?view_only=false')
        assert response.status_code == 200
        response = app_client_user.get(path=f'/accesses/{file_2_id}')
        assert response.status_code == 200
        response = app_client_user.delete(path=f'/reset_access/{file_2_id}')
        assert response.status_code == 200

    def test_set_double_access_url(self, app_client_user):
        response = app_client_user.put(path=f'/set_access/{file_2_id}')
        assert response.status_code == 200
        response = app_client_user.get(path=f'/accesses/{file_2_id}')
        assert response.status_code == 200
        response = app_client_user.put(path=f'/set_access/{file_2_id}')
        assert response.status_code == 200

    def test_add_remove_access_mail_view(self, app_client_user):
        response = app_client_user.put(path=f'/add_access/{file_2_id}/email/admin@mail.com')
        assert response.status_code == 200
        response = app_client_user.get(path=f'/accesses/{file_2_id}')
        assert response.status_code == 200
        response = app_client_user.delete(
            path=f'/remove_access/{file_2_id}/email/admin@mail.com')
        assert response.status_code == 200
        response = app_client_user.delete(
            path=f'/remove_access/{file_2_id}/email/admin@mail.com')
        assert response.status_code == 200
        assert response.json['status'] == "nothing to remove"
        response = app_client_user.put(path=f'/add_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d70/email/admin@mail.com')
        assert response.status_code == 401
        response = app_client_user.delete(
            path='/remove_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d70/email/admin@mail.com')
        assert response.status_code == 401
        # Let's test: user not found
        response = app_client_user.put(path=f'/add_access/{file_2_id}/email/admin1@mail.com')
        assert response.status_code == 404

    def test_add_remove_access_mail_view_directory(self, app_client_user):
        response = app_client_user.put(path=f'/add_access/{dir_3_id}/email/admin@mail.com?view_only=true')
        assert response.status_code == 200
        response = app_client_user.put(path=f'/add_access/{dir_3_id}/email/admin@mail.com?view_only=false')
        assert response.status_code == 200
        response = app_client_user.get(path=f'/accesses/{dir_3_id}')
        assert response.status_code == 200
        response = app_client_user.delete(
            path=f'/remove_access/{dir_3_id}/email/admin@mail.com')
        assert response.status_code == 200
        response = app_client_user.delete(
            path=f'/remove_access/{dir_3_id}/email/admin@mail.com')
        assert response.status_code == 200
        assert response.json['status'] == "nothing to remove"

    def test_add_remove_access_mail_view_2(self, app_client_user):
        response = app_client_user.put(
            path=f'/add_access/{file_2_id}/email/admin@mail.com?view_only=true')
        assert response.status_code == 200
        response = app_client_user.put(
            path=f'/add_access/{file_2_id}/email/admin@mail.com?view_only=false')
        assert response.status_code == 200
        response = app_client_user.put(
            path=f'/add_access/{file_2_id}/email/admin@mail.com?view_only=false')
        assert response.status_code == 200
        response = app_client_user.get(path=f'/accesses/{file_2_id}')
        assert response.status_code == 200
        response = app_client_user.delete(
            path=f'/remove_access/{file_2_id}/email/admin@mail.com')
        assert response.status_code == 200

    def test_add_remove_access_department_view(self, app_client_user):
        response = app_client_user.put(
            path=f'/add_access/{file_2_id}/department/Test_department_1?view_only=true')
        assert response.status_code == 200
        response = app_client_user.put(
            path=f'/add_access/{file_2_id}/department/Test_department_10?view_only=true')
        assert response.status_code == 404
        assert response.json['error'] == 'Department not found'
        response = app_client_user.put(
            path=f'/add_access/{file_2_id}/department/Test_department_1?view_only=false')
        assert response.status_code == 200
        response = app_client_user.put(
            path=f'/add_access/{file_2_id}/department/Test_department_1?view_only=false')
        assert response.status_code == 200
        response = app_client_user.get(path=f'/accesses/{file_2_id}')
        assert response.status_code == 200
        response = app_client_user.delete(
            path=f'/remove_access/{file_2_id}/department/Test_department_1')
        assert response.status_code == 200
        response = app_client_user.delete(
            path=f'/remove_access/{file_2_id}/department/Test_department_10')
        assert response.status_code == 200
        response = app_client_user.put(
            path=f'/add_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d70/department/Test_department_1')
        assert response.status_code == 401
        response = app_client_user.delete(
            path=f'/remove_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d70/department/Test_department_1')
        assert response.status_code == 401

    def test_add_remove_access_department_view_2(self, app_client_user):
        response = app_client_user.put(
            path=f'/add_access/{file_2_id}/department/Test_department_1?view_only=false')
        assert response.status_code == 200
        response = app_client_user.get(path=f'/accesses/{file_2_id}')
        assert response.status_code == 200
        response = app_client_user.delete(
            path=f'/remove_access/{file_2_id}/department/Test_department_1')
        assert response.status_code == 200
        response = app_client_user.delete(
            path=f'/remove_access/{file_2_id}/department/Test_department_1')
        assert response.status_code == 200
        assert response.json['status'] == "nothing to remove"

    def test_add_remove_access_department_view_directory(self, app_client_user):
        response = app_client_user.put(
            path=f'/add_access/{dir_3_id}/department/Test_department_1?view_only=false')
        assert response.status_code == 200
        response = app_client_user.put(
            path=f'/add_access/{dir_3_id}/department/Test_department_1?view_only=true')
        assert response.status_code == 200
        response = app_client_user.get(path=f'/accesses/{dir_3_id}')
        assert response.status_code == 200
        response = app_client_user.delete(
            path=f'/remove_access/{dir_3_id}/department/Test_department_1')
        assert response.status_code == 200
        response = app_client_user.delete(
            path=f'/remove_access/{dir_3_id}/department/Test_department_1')
        assert response.status_code == 200
        assert response.json['status'] == "nothing to remove"

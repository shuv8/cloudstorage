import pytest


class TestAccesses:

    def test_get_access(self, app_client_user):
        response = app_client_user.get(path=f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200

        response = app_client_user.get(path=f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d70')
        assert response.status_code == 401

    def test_set_reset_access_url(self, app_client_user):
        response = app_client_user.put(path=f'/set_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73?view_only=true')
        assert response.status_code == 200
        response = app_client_user.put(path=f'/set_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73?view_only=false')
        assert response.status_code == 200
        response = app_client_user.put(path=f'/set_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73?view_only=false')
        assert response.status_code == 200
        response = app_client_user.get(path=f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200
        response = app_client_user.delete(path=f'/reset_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200
        response = app_client_user.delete(path=f'/reset_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200
        assert response.json['status'] == "nothing to remove"
        response = app_client_user.put(path=f'/set_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d70')
        assert response.status_code == 401
        response = app_client_user.delete(path=f'/reset_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d40')
        assert response.status_code == 401

    def test_set_reset_access_url_2(self, app_client_user):
        response = app_client_user.put(path=f'/set_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73?view_only=false')
        assert response.status_code == 200
        response = app_client_user.get(path=f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200
        response = app_client_user.delete(path=f'/reset_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200

    def test_set_double_access_url(self, app_client_user):
        response = app_client_user.put(path='/set_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200
        response = app_client_user.get(path=f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200
        response = app_client_user.put(path='/set_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200
        assert response.json['status'] == "nothing changed"

    def test_add_remove_access_mail_view(self, app_client_user):
        response = app_client_user.put(path=f'/add_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/email/admin@mail.com')
        assert response.status_code == 200
        response = app_client_user.get(path=f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200
        response = app_client_user.delete(
            path='/remove_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/email/admin@mail.com')
        assert response.status_code == 200
        response = app_client_user.delete(
            path='/remove_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/email/admin@mail.com')
        assert response.status_code == 200
        assert response.json['status'] == "nothing to remove"
        response = app_client_user.put(path=f'/add_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d70/email/admin@mail.com')
        assert response.status_code == 401
        response = app_client_user.delete(
            path='/remove_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d70/email/admin@mail.com')
        assert response.status_code == 401

    def test_add_remove_access_mail_view_2(self, app_client_user):
        response = app_client_user.put(
            path=f'/add_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/email/admin@mail.com?view_only=true')
        assert response.status_code == 200
        response = app_client_user.put(
            path=f'/add_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/email/admin@mail.com?view_only=false')
        assert response.status_code == 200
        response = app_client_user.put(
            path=f'/add_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/email/admin@mail.com?view_only=false')
        assert response.status_code == 200
        response = app_client_user.get(path=f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200
        response = app_client_user.delete(
            path='/remove_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/email/admin@mail.com')
        assert response.status_code == 200

    def test_add_remove_access_department_view(self, app_client_user):
        response = app_client_user.put(
            path=f'/add_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/department/Test_department_1?view_only=true')
        assert response.status_code == 200
        response = app_client_user.put(
            path=f'/add_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/department/Test_department_1?view_only=false')
        assert response.status_code == 200
        response = app_client_user.put(
            path=f'/add_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/department/Test_department_1?view_only=false')
        assert response.status_code == 200
        response = app_client_user.get(path=f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200
        response = app_client_user.delete(
            path=f'/remove_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/department/Test_department_1')
        assert response.status_code == 200
        response = app_client_user.put(
            path=f'/add_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d70/department/Test_department_1')
        assert response.status_code == 401
        response = app_client_user.delete(
            path=f'/remove_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d70/department/Test_department_1')
        assert response.status_code == 401

    def test_add_remove_access_department_view_2(self, app_client_user):
        response = app_client_user.put(
            path=f'/add_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/department/Test_department_1?view_only=false')
        assert response.status_code == 200
        response = app_client_user.get(path=f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200
        response = app_client_user.delete(
            path=f'/remove_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/department/Test_department_1')
        assert response.status_code == 200
        response = app_client_user.delete(
            path=f'/remove_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/department/Test_department_1')
        assert response.status_code == 200
        assert response.json['status'] == "nothing to remove"

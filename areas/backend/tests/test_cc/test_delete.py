import pytest

from tests.test_cc.conftest_constants import root_dir_1_id, file_1_id, dir_2_id


class TestDeleteController:

    def test_delete_file(self, app_client_user):
        response = app_client_user.delete(path=f'/delete/{file_1_id}')
        assert response.status_code == 200

    def test_delete_directory_root(self, app_client_user):
        response = app_client_user.delete(path=f"/delete/{root_dir_1_id}")
        assert response.status_code == 404

    def test_delete_directory(self, app_client_user):
        response = app_client_user.delete(path=f"/delete/{dir_2_id}")
        assert response.status_code == 200

    def test_delete_not_found(self, app_client_user):
        response = app_client_user.delete(path='/delete/4c3b76d1-fe24-4fdf-afdf-7c38adb')
        assert response.status_code == 404

    def test_delete_not_found_space(self, client, fill_db):
        login_data = {'email': 'user2@mail.com', 'password': 'password1'}
        response = client.put('/login', json=login_data)
        assert response.status_code == 200
        response = client.delete(path='/delete/4c3b76d1-fe24-4fdf-afdf-7c38adb')
        assert response.status_code == 404

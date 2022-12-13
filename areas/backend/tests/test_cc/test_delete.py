import pytest

from tests.test_cc.conftest_constants import root_dir_1_id, file_1_id, dir_2_id, dir_3_id, space_1_id, file_5_id


class TestDeleteController:

    def test_delete_file(self, app_client_user):
        response = app_client_user.delete(path=f'/delete/{space_1_id}/{file_1_id}')
        assert response.status_code == 200

    def test_delete_directory_root(self, app_client_user):
        response = app_client_user.delete(path=f"/delete/{space_1_id}/{root_dir_1_id}")
        assert response.status_code == 401

    def test_delete_directory(self, app_client_user):
        response = app_client_user.delete(path=f"/delete/{space_1_id}/{dir_2_id}")
        assert response.status_code == 200

    def test_delete_directory_with_subdirectories(self, app_client_user):
        response = app_client_user.delete(path=f"/delete/{space_1_id}/{dir_3_id}")
        assert response.status_code == 200

    def test_delete_not_found(self, app_client_user):
        response = app_client_user.delete(path=f'/delete/{space_1_id}/bb01bafc-21f1-4af8-89f9-79aa0de840cf')
        assert response.status_code == 404

    def test_delete_not_found_space(self, client, fill_db):
        login_data = {'email': 'user2@mail.com', 'password': 'password1'}
        response = client.put('/login', json=login_data)
        assert response.status_code == 200
        response = client.delete(path=f'/delete/bb01bafc-21f1-4af8-89f9-79aa0de840cf/{dir_3_id}')
        assert response.status_code == 404

    def test_delete_wrong_access(self, client, fill_db):
        login_data = {'email': 'admin@mail.com', 'password': 'password'}
        response = client.put('/login', json=login_data)
        assert response.status_code == 200

        response = client.put(path=f'/add_access/{file_5_id}/email/user@mail.com?view_only=true')
        assert response.status_code == 200

        login_data = {'email': 'user@mail.com', 'password': 'password'}
        response = client.put('/login', json=login_data)
        assert response.status_code == 200

        response = client.get(path=f'/get_spaces')
        assert response.status_code == 200
        all_types = [elem['type'] for elem in response.json['spaces']]
        all_ids = [elem['id'] for elem in response.json['spaces']]
        assert 'Regular' in all_types
        assert 'Shared' in all_types

        response = client.delete(path=f'/delete/{all_ids[1]}/{file_5_id}')
        assert response.status_code == 401
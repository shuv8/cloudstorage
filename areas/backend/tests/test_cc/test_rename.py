import pytest

from tests.test_cc.conftest_constants import space_1_id, file_1_id, dir_2_id, file_5_id, url_space_2_id, dir_5_id


class TestRenameController:

    def test_rename_file(self, app_client_user):
        response = app_client_user.put(path=f'/rename/{space_1_id}/{file_1_id}'
                                       '?new_name=test_name&&scope=test')
        assert response.status_code == 200

    def test_rename_directory(self, app_client_user):
        response = app_client_user.put(path=f'/rename/{space_1_id}/{dir_2_id}'
                                       '?new_name=test_name&&scope=test')
        assert response.status_code == 200

    def test_rename_negative(self, app_client_user):
        response = app_client_user.put(path=f'/rename/{space_1_id}/aaa?new_name=test_name')
        assert response.status_code == 404

        response = app_client_user.put(path=f'/rename/{space_1_id}/{dir_2_id}?wrong_param=test_name')
        assert response.status_code == 400


    def test_rename_wrong_access(self, client, fill_db):
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

        response = client.put(path=f'/rename/{all_ids[1]}/{file_5_id}?new_name=test_name')
        assert response.status_code == 401


    def test_rename_wrong_access_department(self, client, fill_db):
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

        response = client.put(path=f'/rename/{all_ids[1]}/{file_5_id}?new_name=test_name')
        assert response.status_code == 401


    def test_rename_url_access(self, app_client_user):
        response = app_client_user.put(path=f'/rename/{url_space_2_id}/{dir_5_id}?new_name=test_name')
        assert response.status_code == 200

import pytest

from tests.test_cc.conftest_constants import root_dir_1_id, space_1_id, dir_3_id, dir_5_id


class TestBase:

    def test_get_spaces(self, app_client_user):
        response = app_client_user.get(path=f'/get_spaces')
        assert response.status_code == 200

    def test_space_content(self, app_client_user):
        response = app_client_user.get(path=f'/get_space/{space_1_id}')
        assert response.status_code == 200

        response = app_client_user.get(path=f'/get_space/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd0')
        assert response.status_code == 404

    def test_dir_content(self, app_client_user):
        response = app_client_user.get(path=f'/get_dir/{root_dir_1_id}')
        assert response.status_code == 200

        response = app_client_user.get(path=f'/get_dir/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fa0')
        assert response.status_code == 404

    def test_dir_content_sub_sub_folder(self, app_client_user):
        response = app_client_user.get(path=f'/get_dir/{dir_5_id}')
        assert response.status_code == 200

    def test_dir_content_url_space(self, client, fill_db):
        login_data = {'email': 'user2@mail.com', 'password': 'password1'}
        response = client.put('/login', json=login_data)
        assert response.status_code == 200

        response = client.get(path=f'/get_dir/{root_dir_1_id}')
        assert response.status_code == 200

    def test_dir_content_url_space_sub_folder(self, client, fill_db):
        login_data = {'email': 'user2@mail.com', 'password': 'password1'}
        response = client.put('/login', json=login_data)
        assert response.status_code == 200

        response = client.get(path=f'/get_dir/{dir_3_id}')
        assert response.status_code == 200

    def test_dir_content_url_space_sub_sub_folder(self, client, fill_db):
        login_data = {'email': 'user2@mail.com', 'password': 'password1'}
        response = client.put('/login', json=login_data)
        assert response.status_code == 200

        response = client.get(path=f'/get_dir/{dir_5_id}')
        assert response.status_code == 200

    def test_dir_content_url_space_sub_sub_folder_error(self, client, fill_db):
        login_data = {'email': 'user2@mail.com', 'password': 'password1'}
        response = client.put('/login', json=login_data)
        assert response.status_code == 200

        response = client.get(path=f'/get_dir/bbd9cd7f-9ffd-0000-bce4-eb14b51a1f09')
        assert response.status_code == 404

    def test_dir_create(self, app_client_user):
        response = app_client_user.post(
            path=f'/directory', json={
                "space_id": space_1_id,
                "parent_id": root_dir_1_id,
                "new_directory_name": "mega new dir"
            })
        assert response.status_code == 200
        response2 = app_client_user.post(
            path=f'/directory', json={
                "space_id": space_1_id,
                "parent_id": root_dir_1_id,
                "new_directory_name": "mega new dir"
            })
        assert response2.status_code == 403

        new_id = response.json['id']
        response = app_client_user.get(
            path=f'/get_dir/{new_id}')
        assert response.status_code == 200

    def test_dir_create_invalid_json(self, app_client_user):
        response = app_client_user.post(
            path=f'/directory', json={
                "my_space_id": space_1_id,
                "parent_id": root_dir_1_id,
                "new_directory_name": "mega new dir"
            })
        assert response.status_code == 400
        assert response.json['error'] == 'Invalid request body'

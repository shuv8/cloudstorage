import pytest

from tests.test_cc.conftest_constants import root_dir_1_id, dir_2_id, file_1_id, space_1_id, url_space_2_id, dir_5_id, \
    dir_3_id, root_dir_2_id, dir_4_id


class TestMoveController:

    def test_move_file(self, app_client_user):
        response = app_client_user.put(path=f'/move/{space_1_id}/{file_1_id}'
                                            f'?target_directory={dir_2_id}&target_space={space_1_id}')
        assert response.status_code == 200

    def test_move_directory(self, app_client_user):
        response = app_client_user.put(path=f"/move/{space_1_id}/{dir_2_id}"
                                            f"?target_directory={root_dir_1_id}&target_space={space_1_id}")
        assert response.status_code == 200

    def test_move_negative(self, app_client_user):
        response = app_client_user.put(path=f'/move/{space_1_id}/abd9cd7f-9ffd-42b0-bce4-eb14b51a1999'
                                            f'?target_directory={dir_2_id}&target_space={space_1_id}')
        assert response.status_code == 404

        response = app_client_user.put(path=f'/move/{space_1_id}/{dir_2_id}'
                                            f'?target_directory=abd9cd7f-9ffd-42b0-bce4-eb14b51a1999&target_space={space_1_id}')
        assert response.status_code == 404

        response = app_client_user.put(path=f'/move/{space_1_id}/{dir_2_id}?wrong_param=test_name')
        assert response.status_code == 400

        response = app_client_user.put(path=f'/move/fbd9cd7f-9ffd-42b0-bce4-eb14b51a1999/{dir_2_id}?target_directory=abd9cd7f-9ffd-42b0-bce4-eb14b51a1999&target_space={space_1_id}')
        assert response.status_code == 404


    def test_move_url_access(self, app_client_user):
        response = app_client_user.put(path=f'/move/{url_space_2_id}/{dir_5_id}?target_directory={root_dir_1_id}&target_space={space_1_id}')
        assert response.status_code == 200

        response = app_client_user.put(path=f'/move/{space_1_id}/{dir_2_id}?target_directory={dir_3_id}&target_space={url_space_2_id}')
        assert response.status_code == 200

    def test_copy_wrong_access(self, client, fill_db):
        login_data = {'email': 'admin@mail.com', 'password': 'password'}
        response = client.put('/login', json=login_data)
        assert response.status_code == 200

        response = client.put(path=f'/add_access/{root_dir_2_id}/email/user@mail.com?view_only=true')
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

        response = client.put(path=f'/move/{space_1_id}/{dir_3_id}'
                                        f'?target_directory={dir_4_id}'
                                        f'&target_space={all_ids[1]}')
        assert response.status_code == 401

    def test_copy_wrong_access_2(self, client, fill_db):
        login_data = {'email': 'admin@mail.com', 'password': 'password'}
        response = client.put('/login', json=login_data)
        assert response.status_code == 200

        response = client.put(path=f'/add_access/{root_dir_2_id}/email/user@mail.com?view_only=true')
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

        response = client.put(path=f'/move/{all_ids[1]}/{dir_4_id}'
                                        f'?target_directory={dir_3_id}'
                                        f'&target_space={space_1_id}')
        assert response.status_code == 401


import pytest

from tests.test_cc.conftest_constants import url_space_1_id, root_dir_1_id, space_1_id


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
        response = app_client_user.get(
            path=f'/get_dir/{space_1_id}/{root_dir_1_id}')
        assert response.status_code == 200

        response = app_client_user.get(
            path=f'/get_dir/{space_1_id}/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fa0')
        assert response.status_code == 404

        response = app_client_user.get(
            path=f'/get_dir/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd0/{root_dir_1_id}')
        assert response.status_code == 404

    def test_dir_content_url_space(self, app_client_user):
        response = app_client_user.get(
            path=f'/get_dir/{url_space_1_id}/{root_dir_1_id}')
        assert response.status_code == 200

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
            path=f'/get_dir/{space_1_id}/{new_id}')
        assert response.status_code == 200

import pytest


class TestBase:

    def test_get_spaces(self, app_client):
        response = app_client.get(path=f'/get_spaces?scope=test')
        assert response.status_code == 200

    def test_space_content(self, app_client):
        response = app_client.get(path=f'/get_space/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1?scope=test')
        assert response.status_code == 200

        response = app_client.get(path=f'/get_space/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd0?scope=test')
        assert response.status_code == 404

    def test_dir_content(self, app_client):
        response = app_client.get(
            path=f'/get_dir/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fa4?scope=test')
        assert response.status_code == 200

        response = app_client.get(
            path=f'/get_dir/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fa0?scope=test')
        assert response.status_code == 404

        response = app_client.get(
            path=f'/get_dir/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd0/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fa0?scope=test')
        assert response.status_code == 404

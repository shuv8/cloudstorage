import pytest


class TestBase:

    def test_get_spaces(self, app_client_user):
        response = app_client_user.get(path=f'/get_spaces')
        assert response.status_code == 200

    def test_space_content(self, app_client_user):
        response = app_client_user.get(path=f'/get_space/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1')
        assert response.status_code == 200

        response = app_client_user.get(path=f'/get_space/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd0')
        assert response.status_code == 404

    def test_dir_content(self, app_client_user):
        response = app_client_user.get(
            path=f'/get_dir/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1/bb01bafc-21f1-4af8-89f9-79aa0de840c0')
        assert response.status_code == 200

        response = app_client_user.get(
            path=f'/get_dir/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fa0')
        assert response.status_code == 404

        response = app_client_user.get(
            path=f'/get_dir/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd0/bb01bafc-21f1-4af8-89f9-79aa0de840c0')
        assert response.status_code == 404

    def test_dir_content_url_space(self, app_client_user):
        response = app_client_user.get(
            path=f'/get_dir/abd9cd7f-9ffd-41b0-d1e4-eb14b51a6d42/bb01bafc-21f1-4af8-89f9-79aa0de840c0')
        assert response.status_code == 200
import pytest


class TestDeleteController:

    def test_delete_file(self, app_client_user):
        response = app_client_user.delete(path='/delete/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1',
                                           query_string={'scope': 'separate'})
        assert response.status_code == 200

    def test_delete_directory(self, app_client_user):
        response = app_client_user.delete(path='/delete/bb01bafc-21f1-4af8-89f9-79aa0de840c0',
                                           query_string={'scope': 'separate'})
        assert response.status_code == 200

    def test_delete_not_found(self, app_client_user):
        response = app_client_user.delete(path='/delete/4c3b76d1-fe24-4fdf-afdf-7c38adb',
                                           query_string={'scope': 'separate'})
        assert response.status_code == 404

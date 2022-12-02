import pytest


class TestRenameController:

    def test_rename_file(self, app_client):
        response = app_client.put(path='/rename/abd9cd7f-9ffd-41b0-bce4-eb14b51a6d72'
                                       '?new_name=test_name&&scope=test')
        assert response.status_code == 200

    def test_rename_directory(self, app_client):
        response = app_client.put(path='/rename/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1'
                                       '?new_name=test_name&&scope=test')
        assert response.status_code == 200

    def test_rename_negative(self, app_client):
        response = app_client.put(path='/rename/aaa?new_name=test_name')
        assert response.status_code == 404

        response = app_client.put(path='/rename/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1?wrong_param=test_name')
        assert response.status_code == 400

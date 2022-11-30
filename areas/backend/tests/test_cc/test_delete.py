import pytest


@pytest.mark.skip
class TestDeleteController:

    def test_delete_file(self, app_client):
        response = app_client.delete(path='/delete/abd9cd7f-9ffd-41b0-d1e4-eb14b51a6d15')
        assert response.status_code == 200

    def test_delete_directory(self, app_client):
        response = app_client.delete(path='/delete/4c3b76d1-fe24-4fdf-afdf-7c38adbdab15')
        assert response.status_code == 200

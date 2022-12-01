import pytest


class TestViewFileById:

    def test_file_not_found(self, app_client):
        response = app_client.get(f'/file/abd9cd7f-9ffd-42b0-b2d4-eb14b51a6d73/view')
        assert response.status_code == 404
        assert response.text == '{"error":"File not found"}\n'

    def test_file_wrong_type(self, app_client):
        response = app_client.get(f'/file/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/view')
        assert response.status_code == 403
        assert response.text == '{"error":"Cannot view such type of file"}\n'

    def test_file_damaged(self, app_client):
        response = app_client.get(f'/file/abd9cd7d-9ffd-41b0-d1e4-eb14b51a6d72/view?scope=separate')
        assert response.status_code == 404
        assert response.text == '{"error":"File is damaged"}\n'

    def test_file_success(self, app_client):
        response = app_client.get(f'/file/abd9cd7f-9ffd-41b0-d1e4-eb14b51a6d72/view')
        assert response.status_code == 200
        assert response.text == 'TestText'

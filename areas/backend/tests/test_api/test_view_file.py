import pytest

from tests.test_cc.conftest_constants import file_4_id

url = f'http://127.0.0.1:5000'


class TestViewFileById:

    def test_file_not_found(self, api_log_client):
        response = api_log_client._request('GET', url + f'/file/abd9cd7f-9ffd-42b0-b2d4-eb14b51a6d73/view')
        assert response.status_code == 404
        assert response.text == '{"error":"File not found"}\n'

    def test_file_wrong_type(self, api_log_client):
        response = api_log_client._request('GET', url + f'/file/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/view')
        assert response.status_code == 403
        assert response.text == '{"error":"Cannot view such type of file"}\n'

    def test_file_damaged(self, api_log_client):
        response = api_log_client._request('GET', url + f'/file/abd9cd7d-9ffd-41b0-d1e4-eb14b51a6d72/view')
        assert response.status_code == 404
        assert response.text == '{"error":"File is damaged"}\n'

    def test_file_success(self, api_log_client):
        response = api_log_client._request('GET', url + f'/file/{file_4_id}/view')
        assert response.status_code == 200
        assert response.text == 'TestText'

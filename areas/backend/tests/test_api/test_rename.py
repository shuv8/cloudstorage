import pytest

url = f'http://127.0.0.1:5000'


class TestRename:

    def test_rename_file(self, api_log_client):
        response = api_log_client._request('PUT', url + f'/rename/abd9cd7f-9ffd-41b0-bce4-eb14b51a6d72'
                                                        f'?new_name=test_name&&scope=separate')
        assert response.status_code == 200
        assert response.text == '{"new_name":"test_name"}\n'

    def test_rename_directory(self, api_log_client):
        response = api_log_client._request('PUT', url + f'/rename/abd9cd7f-9ffd-42b0-bce4-eb14b51n1jn1'
                                                        f'?new_name=test_name')
        assert response.status_code == 200
        assert response.text == '{"new_name":"test_name"}\n'

    def test_rename_negative(self, api_log_client):
        response = api_log_client._request('PUT', url + f'/rename/aaa'
                                                        f'?new_name=test_name')
        assert response.status_code == 404
        assert response.text == '{"error":"Can\'t find item"}\n'
        response = api_log_client._request('PUT', url + f'/rename/abd9cd7f-9ffd-42b0-bce4-eb14b51n1jn1'
                                                        f'?wrong_param=test_name')
        assert response.status_code == 400
        assert response.text == '{"error":"No new name presented. Use query parameter \'new_name\'"}\n'

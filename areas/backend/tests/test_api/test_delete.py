url = f'http://127.0.0.1:5000'


class TestDelete:

    def test_delete_file(self, api_log_client):
        response = api_log_client._request('DELETE', url + f'/delete/abd9cd7f-9ffd-41b0-bce4-eb14b51a6d72')
        assert response.status_code == 200
        assert response.text == '{"delete":"success"}\n'

    def test_delete_directory(self, api_log_client):
        response = api_log_client._request('DELETE', url + f'/delete/xyz9cd7f-9ffd-42b0-bce4-eb14b51n1jn1')
        assert response.status_code == 200
        assert response.text == '{"delete":"success"}\n'

    def test_delete_negative(self, api_log_client):
        response = api_log_client._request('DELETE', url + f'/delete/aaa')
        assert response.status_code == 400
        assert response.text == '{"error":"Wrong try to delete"}\n'

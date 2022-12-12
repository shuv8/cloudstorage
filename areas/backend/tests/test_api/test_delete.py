from tests.test_cc.conftest_constants import dir_2_id, file_1_id

url = f'http://127.0.0.1:5000'


class TestDelete:

    def test_delete_file(self, api_log_client):
        response = api_log_client._request('DELETE', url + f'/delete/{file_1_id}')
        assert response.status_code == 200
        assert response.text == '{"delete":"success"}\n'

    def test_delete_directory(self, api_log_client):
        response = api_log_client._request('DELETE', url + f'/delete/{dir_2_id}')
        assert response.status_code == 200
        assert response.text == '{"delete":"success"}\n'

    def test_delete_negative(self, api_log_client):
        response = api_log_client._request('DELETE', url + f'/delete/aaa')
        assert response.status_code == 404
        assert response.text == '{"error":"No such file or directory"}\n'

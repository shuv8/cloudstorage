import pytest

from tests.test_cc.conftest_constants import dir_2_id

url = f'http://127.0.0.1:5000'


class TestCopy:

    def test_copy_file(self, api_log_client):
        response = api_log_client._request('POST', url + f'/copy/abd9cd7f-9ffd-41b0-bce4-eb14b51a6d72'
                                                         f'?target_directory=4c3b76d1-fe24-4fdf-afdf-7c38adbdab14')
        assert response.status_code == 200
        assert response.text == '{"new_directory":"second"}\n'

    def test_copy_directory(self, api_log_client):
        response = api_log_client._request('POST', url + f'/copy/4c3b76d1-fe24-4fdf-afdf-7c38adbdab14'
                                                         f'?target_directory={dir_2_id}')
        assert response.status_code == 200
        assert response.text == '{"new_directory":"wow"}\n'

    def test_copy_negative(self, api_log_client):
        response = api_log_client._request('POST', url + f'/copy/aaa'
                                                         f'?target_directory={dir_2_id}')
        assert response.status_code == 404
        assert response.text == '{"error":"Can\'t find one of items"}\n'
        response = api_log_client._request('POST', url + f'/copy/{dir_2_id}'
                                                         f'?target_directory=abd9cd7f-9ffd-42b0-bce4-eb14b51a1999')
        assert response.status_code == 404
        assert response.text == '{"error":"Can\'t find one of items"}\n'
        response = api_log_client._request('POST', url + f'/copy/{dir_2_id}'
                                                         f'?wrong_param=test_name')
        assert response.status_code == 400
        assert response.text == '{"error":"No target directory presented. Use query parameter \'target_directory\'"}\n'

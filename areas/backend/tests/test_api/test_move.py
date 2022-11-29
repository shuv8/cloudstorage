import pytest

url = f'http://127.0.0.1:5000'


class TestMove:

    def test_move_file(self, api_log_client):
        response = api_log_client._request('PUT', url + f'/move/abd9cd7f-9ffd-41b0-bce4-eb14b51a6d72'
                                                        f'?target_directory=4c3b76d1-fe24-4fdf-afdf-7c38adbdab14&&scope=separate')
        print(response.reason)
        assert response.status_code == 200
        assert response.text == '{"new_directory":"second"}\n'

    def test_move_directory(self, api_log_client):
        response = api_log_client._request('PUT', url + f'/move/4c3b76d1-fe24-4fdf-afdf-7c38adbdab14'
                                                        f'?target_directory=abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1'
                                                        f'&&scope=separate')
        assert response.status_code == 200
        assert response.text == '{"new_directory":"wow"}\n'

    def test_move_negative(self, api_log_client):
        response = api_log_client._request('PUT', url + f'/move/abd9cd7f-9ffd-42b0-bce4-eb14b51a1999'
                                                        f'?target_directory=abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1')
        assert response.status_code == 404
        assert response.text == '{"error":"Can\'t find one of items"}\n'
        response = api_log_client._request('PUT', url + f'/move/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1'
                                                        f'?target_directory=abd9cd7f-9ffd-42b0-bce4-eb14b51a1999')
        assert response.status_code == 404
        assert response.text == '{"error":"Can\'t find one of items"}\n'
        response = api_log_client._request('PUT', url + f'/move/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1'
                                                        f'?wrong_param=test_name')
        assert response.status_code == 400
        assert response.text == '{"error":"No target directory presented. Use query parameter \'target_directory\'"}\n'

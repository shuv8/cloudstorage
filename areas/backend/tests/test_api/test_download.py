url = f'http://127.0.0.1:5000'


class TestDownload:

    def test_download_file(self, api_log_client):
        response = api_log_client._request('GET', url + f'/download/abd9cd7f-9ffd-41b0-bce4-eb14b51a6d71')
        assert response.status_code == 200
        assert response.headers['content-disposition'] == 'attachment; filename=image.png'

    def test_download_directory(self, api_log_client):
        response = api_log_client._request('GET', url + f'/download/4c3b76d1-fe24-4fdf-afdf-7c38adbdab15')
        assert response.status_code == 200
        assert response.headers['content-disposition'] == 'attachment; filename=delete'

    def test_download_negative(self, api_log_client):
        response = api_log_client._request('GET', url + f'/download/aaa')
        assert response.status_code == 404
        assert response.text == '{"error":"No such file or directory"}\n'

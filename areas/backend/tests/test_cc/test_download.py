class TestDownloadController:

    def test_download_file(self, app_client):
        response = app_client.get(path='/download/abd9cd7f-9ffd-41b0-bce4-eb14b51a6d71')
        print(app_client)
        assert response.status_code == 200

    def test_download_directory(self, app_client):
        response = app_client.get(path='/download/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1')
        print(app_client)
        assert response.status_code == 200

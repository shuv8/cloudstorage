class TestDownloadController:

    def test_download_file(self, app_client_user):
        response = app_client_user.get(path='/download/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1')
        assert response.status_code == 200

    def test_download_directory(self, app_client_user):
        response = app_client_user.get(path='/download/bb01bafc-21f1-4af8-89f9-79aa0de840c0')
        assert response.status_code == 200

    def test_delete_not_found(self, app_client_user):
        response = app_client_user.get(path='/download/abd9cd7f-9ffd-42b0-bce4-eb14')
        assert response.status_code == 404

class TestDownloadController:

    def test_download_file(self, app_client_admin):
        response = app_client_admin.get(path='/download/abd9cd7f-9ffd-41b0-bce4-eb14b51a6d71')
        print(app_client_admin)
        assert response.status_code == 200

    def test_download_directory(self, app_client_admin):
        response = app_client_admin.get(path='/download/4c3b76d1-fe24-4fdf-afdf-7c38adbdab15')
        print(app_client_admin)
        assert response.status_code == 200

    def test_delete_not_found(self, app_client_admin):
        response = app_client_admin.get(path='/download/abd9cd7f-9ffd-42b0-bce4-eb14')
        print(app_client_admin)
        assert response.status_code == 404

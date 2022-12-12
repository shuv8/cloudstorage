import pytest

from tests.test_cc.conftest_constants import root_dir_1_id, file_1_id


class TestDeleteController:

    def test_delete_file(self, app_client_user):
        response = app_client_user.delete(path=f'/delete/{file_1_id}',
                                          query_string={'scope': 'separate'})
        assert response.status_code == 200

    def test_delete_directory(self, app_client_user):
        response = app_client_user.delete(path=f"/delete/{root_dir_1_id}",
                                           query_string={'scope': 'separate'})
        assert response.status_code == 200

    def test_delete_not_found(self, app_client_user):
        response = app_client_user.delete(path='/delete/4c3b76d1-fe24-4fdf-afdf-7c38adb',
                                           query_string={'scope': 'separate'})
        assert response.status_code == 404

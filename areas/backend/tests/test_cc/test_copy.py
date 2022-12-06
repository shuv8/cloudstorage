import pytest


class TestCopyController:

    def test_copy_file(self, app_client_user):
        response = app_client_user.post(path='/copy/abd9cd7f-9ffd-41b0-bce4-eb14b51a6d72'
                                        '?target_directory=abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1')
        assert response.status_code == 200

    def test_copy_directory(self, app_client_user):
        response = app_client_user.post(path='/copy/bb01bafc-21f1-4af8-89f9-79aa0de840c0'
                                        '?target_directory=abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1')
        assert response.status_code == 200
        assert response.text == '{"new_directory":"Bla"}\n'

    def test_copy_negative(self, app_client_user):
        response = app_client_user.post(path='/copy/aaa?target_directory=abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1')
        assert response.status_code == 404

        response = app_client_user.post(path='/copy/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1'
                                        '?target_directory=abd9cd7f-9ffd-42b0-bce4-eb14b51a1999')
        assert response.status_code == 404

        response = app_client_user.post(path='/copy/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1?wrong_param=test_name')
        assert response.status_code == 400

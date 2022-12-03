import pytest


class TestMoveController:

    def test_move_file(self, app_client):
        response = app_client.put(path='/move/abd9cd7f-9ffd-41b0-bce4-eb14b51a6d72'
                                       '?target_directory=4c3b76d1-fe24-4fdf-afdf-7c38adbdab14')
        assert response.status_code == 200

    def test_move_directory(self, app_client):
        response = app_client.put(path='/move/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1'
                                       '?target_directory=4c3b76d1-fe24-4fdf-afdf-7c38adbdab14')
        assert response.status_code == 200

    def test_move_negative(self, app_client):
        response = app_client.put(path='/move/abd9cd7f-9ffd-42b0-bce4-eb14b51a1999'
                                       '?target_directory=abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1')
        assert response.status_code == 404

        response = app_client.put(path='/move/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1'
                                       '?target_directory=abd9cd7f-9ffd-42b0-bce4-eb14b51a1999')
        assert response.status_code == 404

        response = app_client.put(path='/move/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1'
                                       '?wrong_param=test_name')
        assert response.status_code == 400

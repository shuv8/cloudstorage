import pytest

from tests.test_cc.conftest_constants import root_dir_1_id, dir_2_id, file_1_id, space_1_id


class TestMoveController:

    def test_move_file(self, app_client_user):
        response = app_client_user.put(path=f'/move/{space_1_id}/{file_1_id}'
                                            f'?target_directory={dir_2_id}&target_space={space_1_id}')
        assert response.status_code == 200

    def test_move_directory(self, app_client_user):
        response = app_client_user.put(path=f"/move/{space_1_id}/{dir_2_id}"
                                            f"?target_directory={root_dir_1_id}&target_space={space_1_id}")
        assert response.status_code == 200

    def test_move_negative(self, app_client_user):
        response = app_client_user.put(path=f'/move/{space_1_id}/abd9cd7f-9ffd-42b0-bce4-eb14b51a1999'
                                            f'?target_directory={dir_2_id}&target_space={space_1_id}')
        assert response.status_code == 404

        response = app_client_user.put(path=f'/move/{space_1_id}/{dir_2_id}'
                                            f'?target_directory=abd9cd7f-9ffd-42b0-bce4-eb14b51a1999&target_space={space_1_id}')
        assert response.status_code == 404

        response = app_client_user.put(path=f'/move/{space_1_id}/{dir_2_id}?wrong_param=test_name')
        assert response.status_code == 400

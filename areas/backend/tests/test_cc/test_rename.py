import pytest

from tests.test_cc.conftest_constants import space_1_id, file_1_id, dir_2_id


class TestRenameController:

    def test_rename_file(self, app_client_user):
        response = app_client_user.put(path=f'/rename/{space_1_id}/{file_1_id}'
                                       '?new_name=test_name&&scope=test')
        assert response.status_code == 200

    def test_rename_directory(self, app_client_user):
        response = app_client_user.put(path=f'/rename/{space_1_id}/{dir_2_id}'
                                       '?new_name=test_name&&scope=test')
        assert response.status_code == 200

    def test_rename_negative(self, app_client_user):
        response = app_client_user.put(path=f'/rename/{space_1_id}/aaa?new_name=test_name')
        assert response.status_code == 404

        response = app_client_user.put(path=f'/rename/{space_1_id}/{dir_2_id}?wrong_param=test_name')
        assert response.status_code == 400

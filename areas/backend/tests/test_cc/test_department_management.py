import pytest

from tests.test_cc.conftest_constants import admin_id, casual_user_id


class TestDepartmentManagement:

    def test_wrong_json(self, app_client_admin):
        wrong_json = {
            "department": "Test_name1"
        }
        response = app_client_admin.post(f'/department', json=wrong_json)
        assert response.status_code == 400
        assert response.text == '{"error":"Invalid request body"}\n'

    def test_already_exists(self, app_client_admin):
        data = {
            "department_name": "Test_department_2"
        }
        response = app_client_admin.post(f'/department', json=data)
        assert response.status_code == 400
        assert response.text == '{"error":"Already exists department with such name"}\n'

    def test_get_department_lists(self, app_client_admin):
        response = app_client_admin.get(f'/department')
        assert response.status_code == 200
        response_data = response.json
        assert 'departments' in response_data
        assert len(response_data['departments']) == 2

    def test_creation_success(self, app_client_admin):
        data = {
            "department_name": "Test_department_3"
        }
        response = app_client_admin.post(f'/department', json=data)
        assert response.status_code == 200
        response = app_client_admin.get(f'/department')
        assert response.status_code == 200
        response_data = response.json
        assert 'departments' in response_data
        assert len(response_data['departments']) == 3

    def test_get_department_lists_with_query(self, app_client_admin):
        response = app_client_admin.get(f'/department?page=2')
        assert response.status_code == 200
        response_data = response.json
        assert 'departments' in response_data
        assert len(response_data['departments']) == 0

        response = app_client_admin.get(f'/department?page=2&limit=1')
        assert response.status_code == 200
        response_data = response.json
        assert 'departments' in response_data
        assert len(response_data['departments']) == 1

    def test_delete_department_wrong_data(self, app_client_admin):
        wrong_json = {
            "department": "Test_name1"
        }
        response = app_client_admin.delete(f'/department', json=wrong_json)
        assert response.status_code == 400
        assert response.text == '{"error":"Invalid request body"}\n'

    def test_delete_department_not_found(self, app_client_admin):
        data = {
            "department_name": "Test_department_4"
        }
        response = app_client_admin.delete(f'/department', json=data)
        assert response.status_code == 404
        assert response.text == '{"error":"Department with such name doesnt exist"}\n'

    def test_delete_department_success(self, app_client_admin):
        data = {
            "department_name": "Test_department_2"
        }
        response = app_client_admin.delete(f'/department', json=data)
        assert response.status_code == 200

        response = app_client_admin.get(f'/department')
        assert response.status_code == 200
        response_data = response.json
        assert 'departments' in response_data
        assert len(response_data['departments']) == 1

    def test_access_denied(self, app_client_user):
        response = app_client_user.get(f'/department')
        assert response.status_code == 403
        assert response.text == '{"error":"access denied"}\n'

    def test_get_departments_with_users(self, app_client_admin):
        response = app_client_admin.get(f'/department/users?name=Test_department_1')
        response_data = response.json
        assert response.status_code == 200
        assert response_data["department_name"] == "Test_department_1"
        assert response_data["users"] == []

    def test_get_departments_with_users_nf(self, app_client_admin):
        response = app_client_admin.get(f'/department/users?name=Test_department_3')
        response_data = response.json
        assert response.status_code == 404
        assert response_data["error"] == 'Department with such name doesnt exist'

    def test_add_users_to_department(self, app_client_admin):
        data = {
            "users": [
                casual_user_id,
                admin_id
            ]
        }
        response = app_client_admin.post(f'/department/users?name=Test_department_1',
                                         json=data)
        assert response.status_code == 200

        response = app_client_admin.get(f'/department/users?name=Test_department_1')
        response_data = response.json
        assert response.status_code == 200
        assert response_data["department_name"] == "Test_department_1"
        assert len(response_data["users"]) == 2
        all_ids = [ids["id"] for ids in response_data["users"]]
        all_email = [ids["email"] for ids in response_data["users"]]
        assert casual_user_id in all_ids
        assert admin_id in all_ids
        assert "admin@mail.com" in all_email
        assert "user@mail.com" in all_email

    def test_add_users_to_department_nf(self, app_client_admin):
        data = {
            "users": [
                "bb01bafc-21f1-4af8-89f9-79aa0de840c4",
                admin_id
            ]
        }
        response = app_client_admin.post(f'/department/users?name=Test_department_1',
                                         json=data)
        assert response.status_code == 404

        response = app_client_admin.get(f'/department/users?name=Test_department_1')
        response_data = response.json
        assert response.status_code == 200
        assert response_data["department_name"] == "Test_department_1"
        assert len(response_data["users"]) == 0

        data = {
            "users_1": [
                "bb01bafc-21f1-4af8-89f9-79aa0de840c4",
                admin_id
            ]
        }
        response = app_client_admin.post(f'/department/users?name=Test_department_1',
                                         json=data)
        assert response.status_code == 400
        assert response.json["error"] == 'invalid request body'

        data = {
            "users": [
                "bb01bafc-21f1-4af8-89f9-79aa0de840c4",
                admin_id
            ]
        }
        response = app_client_admin.post(f'/department/users?name=Test_department_3',
                                         json=data)
        assert response.status_code == 404
        assert response.json["error"] == 'Department with such name doesnt exist'

    def test_delete_users_from_department(self, app_client_admin):
        data = {
            "users": [
                casual_user_id,
                admin_id
            ]
        }
        response = app_client_admin.post(f'/department/users?name=Test_department_2',
                                         json=data)
        assert response.status_code == 200

        response = app_client_admin.get(f'/department/users?name=Test_department_2')
        response_data = response.json
        assert response.status_code == 200
        assert response_data["department_name"] == "Test_department_2"
        assert len(response_data["users"]) == 2
        all_ids = [ids["id"] for ids in response_data["users"]]
        assert casual_user_id in all_ids
        assert admin_id in all_ids

        data = {
            "users": [
                casual_user_id,
                "bb01bafc-21f1-4af8-89f9-79aa0de840c7"
            ]
        }
        response = app_client_admin.delete(f'/department/users?name=Test_department_2',
                                           json=data)
        assert response.status_code == 200

        response = app_client_admin.get(f'/department/users?name=Test_department_2')
        response_data = response.json
        assert response.status_code == 200
        assert response_data["department_name"] == "Test_department_2"
        assert len(response_data["users"]) == 1
        all_ids = [ids["id"] for ids in response_data["users"]]
        assert casual_user_id not in all_ids
        assert admin_id in all_ids

    def test_delete_users_from_department_nf(self, app_client_admin):
        data = {
            "users_1": [
                casual_user_id,
                admin_id
            ]
        }
        response = app_client_admin.delete(f'/department/users?name=Test_department_2',
                                         json=data)
        assert response.status_code == 400
        assert response.json["error"] == 'invalid request body'

        data = {
            "users": [
                casual_user_id,
                admin_id
            ]
        }
        response = app_client_admin.delete(f'/department/users?name=Test_department_4',
                                         json=data)
        assert response.status_code == 404
        assert response.json["error"] == 'Department with such name doesnt exist'

    def test_get_users_lists(self, app_client_admin):
        response = app_client_admin.get(f'/user')
        assert response.status_code == 200
        response_data = response.json
        assert 'users' in response_data
        assert len(response_data['users']) == 2
        all_ids = [ids["id"] for ids in response_data["users"]]
        all_email = [ids["email"] for ids in response_data["users"]]
        assert casual_user_id in all_ids
        assert admin_id in all_ids
        assert "admin@mail.com" in all_email
        assert "user@mail.com" in all_email

        response = app_client_admin.get(f'/user?page=3')
        assert response.status_code == 200
        response_data = response.json
        assert 'users' in response_data
        assert len(response_data['users']) == 0

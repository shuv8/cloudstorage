import pytest


class TestDepartmentManagement:

    def test_wrong_json(self, app_client):
        wrong_json = {
            "department": "Test_name1"
        }
        response = app_client.post(f'/department', json=wrong_json)
        assert response.status_code == 400
        assert response.text == '{"error":"Invalid request body"}\n'

    def test_already_exists(self, app_client):
        data = {
            "department_name": "Test_department_2"
        }
        response = app_client.post(f'/department', json=data)
        assert response.status_code == 400
        assert response.text == '{"error":"Already exists department with such name"}\n'

    def test_get_department_lists(self, app_client):
        response = app_client.get(f'/department')
        assert response.status_code == 200
        response_data = response.json
        assert 'departments' in response_data
        assert len(response_data['departments']) == 2

    def test_creation_success(self, app_client):
        data = {
            "department_name": "Test_department_3"
        }
        response = app_client.post(f'/department', json=data)
        assert response.status_code == 200
        response = app_client.get(f'/department')
        assert response.status_code == 200
        response_data = response.json
        assert 'departments' in response_data
        assert len(response_data['departments']) == 3

    def test_get_department_lists_with_query(self, app_client):
        response = app_client.get(f'/department?page=2')
        assert response.status_code == 200
        response_data = response.json
        assert 'departments' in response_data
        assert len(response_data['departments']) == 0

        response = app_client.get(f'/department?page=2&limit=1')
        assert response.status_code == 200
        response_data = response.json
        assert 'departments' in response_data
        assert len(response_data['departments']) == 1

    def test_delete_department_wrong_data(self, app_client):
        wrong_json = {
            "department": "Test_name1"
        }
        response = app_client.delete(f'/department', json=wrong_json)
        assert response.status_code == 400
        assert response.text == '{"error":"Invalid request body"}\n'

    def test_delete_department_not_found(self, app_client):
        data = {
            "department_name": "Test_department_4"
        }
        response = app_client.delete(f'/department', json=data)
        assert response.status_code == 404
        assert response.text == '{"error":"Department with such name doesnt exist"}\n'

    def test_delete_department_success(self, app_client):
        data = {
            "department_name": "Test_department_2"
        }
        response = app_client.delete(f'/department', json=data)
        assert response.status_code == 200

        response = app_client.get(f'/department')
        assert response.status_code == 200
        response_data = response.json
        assert 'departments' in response_data
        flag = False
        for elem in response_data['departments']:
            if elem['department_name'] == data['department_name']:
                flag = True
        assert not flag

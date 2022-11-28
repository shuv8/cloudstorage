import pytest
import json

url = f'http://127.0.0.1:5000'


class TestDepartmentManagement:

    def test_wrong_json(self, api_log_client):
        wrong_json = {
            "department": "Test_name1"
        }
        response = api_log_client._request('POST', url + f'/department', json=wrong_json)
        assert response.status_code == 400
        assert response.text == '{"error":"Invalid request body"}\n'

    def test_already_exists(self, api_log_client):
        data = {
            "department_name": "Test_department_2"
        }
        response = api_log_client._request('POST', url + f'/department', json=data)
        assert response.status_code == 400
        assert response.text == '{"error":"Already exists department with such name"}\n'

    def test_get_department_lists(self, api_log_client):
        response = api_log_client._request('GET', url + f'/department')
        assert response.status_code == 200
        response_data = response.json()
        assert 'departments' in response_data
        assert len(response_data['departments']) == 2

    def test_creation_success(self, api_log_client):
        data = {
            "department_name": "Test_department_3"
        }
        response = api_log_client._request('POST', url + f'/department', json=data)
        assert response.status_code == 200
        response = api_log_client._request('GET', url + f'/department')
        assert response.status_code == 200
        response_data = response.json()
        assert 'departments' in response_data
        assert len(response_data['departments']) == 3

    def test_get_department_lists_with_query(self, api_log_client):
        response = api_log_client._request('GET', url + f'/department'
                                                        f'?page=2')
        assert response.status_code == 200
        response_data = response.json()
        assert 'departments' in response_data
        assert len(response_data['departments']) == 0

        response = api_log_client._request('GET', url + f'/department'
                                                        f'?page=2&limit=1')
        assert response.status_code == 200
        response_data = response.json()
        assert 'departments' in response_data
        assert len(response_data['departments']) == 1

    def test_delete_department_wrong_data(self, api_log_client):
        wrong_json = {
            "department": "Test_name1"
        }
        response = api_log_client._request('DELETE', url + f'/department', json=wrong_json)
        assert response.status_code == 400
        assert response.text == '{"error":"Invalid request body"}\n'

    def test_delete_department_not_found(self, api_log_client):
        data = {
            "department_name": "Test_department_4"
        }
        response = api_log_client._request('DELETE', url + f'/department', json=data)
        assert response.status_code == 404
        assert response.text == '{"error":"Department with such name doesnt exist"}\n'

    def test_delete_department_success(self, api_log_client):
        data = {
            "department_name": "Test_department_2"
        }
        response = api_log_client._request('DELETE', url + f'/department', json=data)
        assert response.status_code == 200

        response = api_log_client._request('GET', url + f'/department')
        assert response.status_code == 200
        response_data = response.json()
        assert 'departments' in response_data
        flag = False
        for elem in response_data['departments']:
            if elem['department_name'] == data['department_name']:
                flag = True
        assert not flag

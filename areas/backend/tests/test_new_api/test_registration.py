import pytest


class TestRegistration:

    def test_wrong_json(self, client):
        wrong_json = {
            "my_email": "test_email@gmail.com",
            "password": "test_pass",
            "role": 1,
            "username": "test_user"
        }
        response = client.post(f'/registration', json=wrong_json)
        assert response.status_code == 400
        resp = response.json
        assert resp['error'] == "Invalid request body"

    def test_already_exist(self, client):
        data = {
            "email": "admin@mail.com",
            "password": "test_pass",
            "role": 1,
            "username": "test_user"
        }
        response = client.post(f'/registration', json=data)
        assert response.status_code == 403
        resp = response.json
        assert resp['error'] == "Email already exists"

    def test_success(self, client):
        data = {
            "email": "test_email@mail.com",
            "password": "test_pass",
            "role": 1,
            "username": "test_user"
        }
        response = client.post(f'/registration', json=data)
        assert response.status_code == 200

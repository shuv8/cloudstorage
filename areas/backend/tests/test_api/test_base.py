import json

import pytest

url = f'http://127.0.0.1:5000'


class TestBase:

    def test_get_spaces(self, api_log_client):
        response = api_log_client._request(
            'GET', url + f'/get_spaces?scope=test'
        )
        assert response.status_code == 200

        result = json.loads(response.text)['spaces']
        assert len(result) == 2

        assert result[0]["name"] == "Main"
        assert result[0]["type"] == "Regular"

        assert result[1]["name"] == "test1"
        assert result[1]["type"] == "Shared"

    def test_space_content(self, api_log_client):
        response = api_log_client._request(
            'GET', url + f'/get_space/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1?scope=test'
        )
        assert response.status_code == 200

        result = json.loads(response.text)['items']
        assert len(result) == 2

        assert result[0]["entity"] == "directory"
        assert result[0]["name"] == "test1"

        assert result[1]["entity"] == "file"
        assert result[1]["name"] == "test2"
        assert result[1]["type"] == ".ty"

    def test_dir_content(self, api_log_client):
        response = api_log_client._request(
            'GET',
            url + f'/get_dir/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fd1/abd9cd7f-9ffd-42b0-bce4-eb14b51a1fa4?scope=test'
        )
        assert response.status_code == 200

        result = json.loads(response.text)['items']
        assert len(result) == 2

        assert result[0]["entity"] == "file"
        assert result[0]["name"] == "test42"
        assert result[0]["type"] == ".ty"

        assert result[0]["entity"] == "directory"
        assert result[0]["name"] == "test4242"

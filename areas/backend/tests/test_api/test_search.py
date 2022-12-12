import json

import pytest

url = f'http://127.0.0.1:5000'


class TestSearch:

    def test_search_file(self, api_log_client):
        response = api_log_client._request('GET', url + f'/search?query=test&scope=access')
        assert response.status_code == 200

        result = json.loads(response.text)['items']
        assert len(result) == 3

        for item in result:
            assert "test" in item["name"]

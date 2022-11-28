import json

url = f'http://127.0.0.1:5000'


class TestRename:

    def test_rename_file(self, api_log_client):
        response = api_log_client._request('GET', url + f'/search'
                                                        f'?query=test')
        assert response.status_code == 200

        result = json.loads(response.text)['items']
        assert len(result) == 5

        for item in result:
            assert "test" in item["name"]

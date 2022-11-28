import json

import pytest

from tests.test_api.mock.database_for_access_tests import DatabaseForAccessTests

url = f'http://127.0.0.1:5000'

import app_states_for_test


class TestSearch:
    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        # Before
        app_states_for_test.is_test = True
        app_states_for_test.test_state = DatabaseForAccessTests()

        yield

        # After
        app_states_for_test.is_test = None

    def pytest_configure(self):
        pytest.is_test = True
        pytest.test_local = DatabaseForAccessTests()

    def test_search_file(self, api_log_client):
        response = api_log_client._request('GET', url + f'/search?query=test&scope=access')
        assert response.status_code == 200

        result = json.loads(response.text)['items']
        assert len(result) == 3

        for item in result:
            assert "test" in item["name"]

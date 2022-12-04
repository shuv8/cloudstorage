import pytest


class TestSearch:

    def test_search(self, app_client_admin):
        response = app_client_admin.get(path=f'/search?query=test&scope=access')
        assert response.status_code == 200

        response = app_client_admin.get(path=f'/search?query=pooooooooooooooower&scope=access')
        assert response.status_code == 200

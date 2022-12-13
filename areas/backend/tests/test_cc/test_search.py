import pytest


class TestSearch:

    def test_search(self, app_client_user):
        response = app_client_user.get(path=f'/search?query=test')
        assert response.status_code == 200

        response = app_client_user.get(path=f'/search?query=Bla')
        assert response.status_code == 200

        response = app_client_user.get(path=f'/search?query=Bl2')
        assert response.status_code == 200

        response = app_client_user.get(path=f'/search?query=pooooooooooooooower')
        assert response.status_code == 200

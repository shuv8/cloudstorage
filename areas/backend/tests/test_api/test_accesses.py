import json

import pytest

url = f'http://127.0.0.1:5000'


class TestRename:

    @pytest.mark.order1
    def test_get_access(self, api_log_client):
        response = api_log_client._request('GET', url + f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200

        result = json.loads(response.text)['accesses']
        assert len(result) == 0

    @pytest.mark.order2
    def test_set_reset_access_url(self, api_log_client):
        # Set URL access
        response = api_log_client._request('PUT', url + f'/set_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200

        # Check URL result
        response = api_log_client._request('GET', url + f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200

        result = json.loads(response.text)['accesses']
        assert len(result) == 1

        # Reset URL access
        response = api_log_client._request('DELETE', url + f'/reset_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200

        # Check URL result

        response = api_log_client._request('GET', url + f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200

        result = json.loads(response.text)['accesses']
        assert len(result) == 0

    @pytest.mark.order3
    def test_set_double_access_url(self, api_log_client):
        # Set URL access
        response = api_log_client._request('PUT', url + f'/set_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200

        # Set URL access
        response = api_log_client._request('GET', url + f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200

        result = json.loads(response.text)['accesses']
        assert len(result) == 1

        # Set URL access
        response = api_log_client._request('PUT', url + f'/set_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 403

        # Check URL result

        response = api_log_client._request('GET', url + f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200

        # Reset URL access
        response = api_log_client._request('DELETE', url + f'/reset_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200

        # Set URL access
        response = api_log_client._request('GET', url + f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200
        result = json.loads(response.text)['accesses']
        assert len(result) == 0

    @pytest.mark.order4
    def test_set_reset_access_url_edit(self, api_log_client):
        # Set URL access
        response = api_log_client._request(
            'PUT',
            url + f'/set_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73?view_only=false'
        )
        assert response.status_code == 200

        # Check URL result
        response = api_log_client._request('GET', url + f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200

        result = json.loads(response.text)['accesses']
        assert len(result) == 1
        assert len(result) == 1
        assert result[0]['type'] == "Edit"
        assert result[0]['class'] == "<class 'core.accesses.UrlAccess'>"

        # Reset URL access
        response = api_log_client._request(
            'DELETE',
            url + f'/reset_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73'
        )
        assert response.status_code == 200

        # Check URL result

        response = api_log_client._request('GET', url + f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200

        result = json.loads(response.text)['accesses']
        assert len(result) == 0

    @pytest.mark.order5
    def test_add_remove_access_mail_view(self, api_log_client):
        # Set mail access
        response = api_log_client._request(
            'PUT',
            url + f'/add_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/email/test_mail@mail.com'
        )
        assert response.status_code == 200

        # Check mail result
        response = api_log_client._request('GET',
                                           url + f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73?view_only=true')
        assert response.status_code == 200

        result = json.loads(response.text)['accesses']
        assert len(result) == 1
        assert result[0]['type'] == "View"
        assert result[0]['class'] == "<class 'core.accesses.UserAccess'>"

        # Reset mail access
        response = api_log_client._request(
            'DELETE',
            url + f'/remove_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/email/test_mail@mail.com'
        )
        assert response.status_code == 200

        # Check mail result

        response = api_log_client._request('GET', url + f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200

        result = json.loads(response.text)['accesses']
        assert len(result) == 0

    @pytest.mark.order6
    def test_add_remove_access_mail_edit(self, api_log_client):
        # Set mail access
        response = api_log_client._request(
            'PUT',
            url + f'/add_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/email/test_mail@mail.com?view_only=false'
        )
        assert response.status_code == 200

        # Check mail result
        response = api_log_client._request('GET', url + f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200

        result = json.loads(response.text)['accesses']
        assert len(result) == 1
        assert result[0]['type'] == "Edit"
        assert result[0]['class'] == "<class 'core.accesses.UserAccess'>"

        # Reset mail access
        response = api_log_client._request(
            'DELETE',
            url + f'/remove_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/email/test_mail@mail.com'
        )
        assert response.status_code == 200

        # Check mail result

        response = api_log_client._request('GET', url + f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200

        result = json.loads(response.text)['accesses']
        assert len(result) == 0

    @pytest.mark.order7
    def test_add_remove_access_department_view(self, api_log_client):
        # Set mail access
        response = api_log_client._request(
            'PUT',
            url + f'/add_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/department/test'
        )
        assert response.status_code == 200

        # Check mail result
        response = api_log_client._request('GET',
                                           url + f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73?view_only=true')
        assert response.status_code == 200

        result = json.loads(response.text)['accesses']
        assert len(result) == 1
        assert result[0]['type'] == "View"
        assert result[0]['class'] == "<class 'core.accesses.DepartmentAccess'>"

        # Reset mail access
        response = api_log_client._request(
            'DELETE',
            url + f'/remove_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/department/test'
        )
        assert response.status_code == 200

        # Check mail result

        response = api_log_client._request('GET', url + f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200

        result = json.loads(response.text)['accesses']
        assert len(result) == 0

    @pytest.mark.order8
    def test_add_remove_access_department_edit(self, api_log_client):
        # Set mail access
        response = api_log_client._request(
            'PUT',
            url + f'/add_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/department/test?view_only=false'
        )
        assert response.status_code == 200

        # Check mail result
        response = api_log_client._request('GET', url + f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200

        result = json.loads(response.text)['accesses']
        assert len(result) == 1
        assert result[0]['type'] == "Edit"
        assert result[0]['class'] == "<class 'core.accesses.DepartmentAccess'>"

        # Reset mail access
        response = api_log_client._request(
            'DELETE',
            url + f'/remove_access/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73/department/test'
        )
        assert response.status_code == 200

        # Check mail result

        response = api_log_client._request('GET', url + f'/accesses/abd9cd7f-9ffd-42b0-bce4-eb14b51a6d73')
        assert response.status_code == 200

        result = json.loads(response.text)['accesses']
        assert len(result) == 0

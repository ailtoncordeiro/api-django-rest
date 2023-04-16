import pytest

def test_list_users(api_client, user_login):
    user, token = user_login
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    response = api_client.get('/api/v1/users')
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_user_fail(api_client):
    response = api_client.post('/api/v1/login/', dict(email="notexist@blabla.com", password='someone'))
    assert response.status_code == 401
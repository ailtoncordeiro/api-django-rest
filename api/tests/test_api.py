import pytest
import json
from rest_framework.test import APIClient

def test_list_users_with_jwt_token(django_user_model):
    # cria um usuário válido para autenticar
    user = django_user_model.objects.create_user(
        name='test user',
        email='testuser@test.com',
        password='testpass'
    )

    # configura o cliente de API
    api_client = APIClient()

    # faz uma solicitação de login para obter um token JWT
    login_data = {
        'email': user.email,
        'password': 'testpass'
    }
    response = api_client.post('/api/v1/login/', data=login_data)
    assert response.status_code == 200
    token = json.loads(response.content.decode('utf-8'))['access']
    # usa o token JWT para fazer uma solicitação para listar todos os usuários
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    response = api_client.get('/api/v1/users')
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_user_fail():

    api_client = APIClient()
    response = api_client.post('/api/v1/login/', dict(email="notexist@blabla.com", password='someone'))

    assert response.status_code == 401
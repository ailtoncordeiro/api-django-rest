import pytest
import json
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_login(django_user_model, api_client):
    user = django_user_model.objects.create_user(
        name='test user',
        email='testuser@test.com',
        password='testpass'
    )
    login_data = {
        'email': user.email,
        'password': 'testpass'
    }
    response = api_client.post('/api/v1/login/', data=login_data)
    token = json.loads(response.content.decode('utf-8'))['access']
    
    return user, token

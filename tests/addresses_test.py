import pytest
from api.models import Addresses

@pytest.mark.django_db
def test_address_user_view_success(api_client, user_login):
    user, token = user_login
    # cria um endereço associado ao usuário autenticado
    address = Addresses.objects.create(
            userID_id=user.id,
            description='Casa',
            postalCode='00000000',
            street='Rua A',
            complement='Apto 101',
            neighborhood='Bairro X',
            city='Cidade Y',
            state='SP'
        )

    # faz a requisição para a view
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    response = api_client.get(f'/api/v1/addresses/userid/{user.id}')

    # verifica se a resposta foi bem sucedida e se o endereço está na resposta
    assert response.status_code == 200
    # Verifica se o endereço criado foi retornado na lista de endereços
    response_data = response.data
    del response_data[0]['createdAt']
    del response_data[0]['updatedAt']
    assert response_data[0]['description'] == 'Casa'
    assert response_data[0]['postalCode'] == '00000000'
    assert response_data[0]['street'] == 'Rua A'
    assert response_data[0]['complement'] == 'Apto 101'
    assert response_data[0]['neighborhood'] == 'Bairro X'
    assert response_data[0]['city'] == 'Cidade Y'
    assert response_data[0]['state'] == 'SP'

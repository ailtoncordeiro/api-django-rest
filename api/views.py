import requests
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework.decorators import action, api_view
from rest_framework.views import APIView
from django.http import Http404

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Addresses.objects.all()
    serializer_class = AddressSerializier
    permission_classes = [permissions.IsAuthenticated]

@extend_schema(
    description="Returns a set of addresses associated with a specific user."
)
class AddressUserView(APIView):

    serializer_class = AddressSerializier
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, userid):
        queryset = Addresses.objects.filter(userID_id=userid).order_by('id')
        serializer = AddressSerializier(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

@extend_schema(
    description="Return an address associated with a postal code"
)
class AddressCepView(APIView):

    serializer_class = AddressSerializier
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, cep):
        postalCode = str(cep)
        postalCode = postalCode.replace("-", "").replace(".", "").replace(" ", "")
        url = f'https://viacep.com.br/ws/{postalCode}/json/'
        if len(postalCode) == 8:
            try:
                data = requests.get(url)
                dataDic = data.json()
                if 'erro' in dataDic and dataDic['erro']:
                    error = {
                        'error': 'Postal code not found.'
                    }
                    return Response(error, status=status.HTTP_404_NOT_FOUND)
                else:
                    addressData = {
                        'street': dataDic['logradouro'],
                        'neighborhood': dataDic['bairro'],
                        'city': dataDic['localidade'],
                        'state': dataDic['uf'],
                        'postalCode': dataDic['cep']
                    }
                    return Response(addressData, status=status.HTTP_200_OK)
            except:
                error = {
                    'error': 'An error occurred while processing the request.'
                }
                return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            error = {
                'error': 'Invalid postal code.'
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializier
    permission_classes = [permissions.IsAuthenticated]

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializier
    permission_classes = [permissions.IsAuthenticated]

class ProductsCategoriesViewSet(viewsets.ModelViewSet):
    queryset = ProductsCategories.objects.all()
    serializer_class = ProductsCategoriesSerialiizer
    permission_classes = [permissions.IsAuthenticated]

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerialiizer
    permission_classes = [permissions.IsAuthenticated]

class OrderItemsViewSet(viewsets.ModelViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerialiizer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Obtém os dados do pedido da solicitação
        data = request.data

        # Obtém o preço do produto correspondente
        product = Products.objects.get(id=data['productID'])
        price = product.price

        # Multiplica o preço pelo quantidade
        quantity = data['quantity']
        calculated_price = price * quantity

        # Adiciona o preço calculado aos dados do pedido
        data['price'] = calculated_price

        # Cria o novo objeto OrderItems com os dados atualizados
        serializer = OrderItemsSerialiizer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
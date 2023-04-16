import requests
from decimal import Decimal, ROUND_HALF_UP
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from django.utils.dateparse import parse_date

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

    @extend_schema(request=CreateOrderItemsSerializer)
    def create(self, request, *args, **kwargs):
        # Obtém os dados do pedido da solicitação
        data = request.data

        # Obtém o preço do produto correspondente
        product = Products.objects.get(id=data['productID'])
        price = product.price

        # Adiciona o preço aos dados do pedido
        data['price'] = price

        # Cria o novo objeto OrderItems com os dados atualizados
        serializer = OrderItemsSerialiizer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class UserOrdersView(RetrieveAPIView):

    queryset = Users.objects.all()
    serializer_class = UserOrdersSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='start_date', 
                type=OpenApiTypes.DATE, 
                location=OpenApiParameter.QUERY,
                description='Start date in YYYY-MM-DD format',
            ),
            OpenApiParameter(
                name='end_date',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='End date in YYYY-MM-DD format',
                
            ),
        ],
        request=None,
    )
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        orders = Orders.objects.filter(userID_id=user)
        if not orders:
            return Response({'message': 'No orders found for this user.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            if start_date:
                orders = orders.filter(createdAt__gte=parse_date(start_date))
            if end_date:
                orders = orders.filter(createdAt__lte=parse_date(end_date))
            orders = orders.select_related('addressesID').prefetch_related('orderitems_set__productID')
            result = []
            order_id = None # Inicializa a variável order_id para evitar erro no final do loop
            for order in orders:
                address = order.addressesID
                items_dict = {}
                order_total_price = Decimal(0)
                try:
                    for item in order.orderitems_set.all():
                        product = item.productID
                        order_id = order.id
                        item_price = product.price * item.quantity
                        order_total_price += item_price
                        if order_id in items_dict:
                            # Se já existe uma entrada para esse pedido, atualiza apenas as informações do item
                            items_dict[order_id]['items'].append({
                                'product_name': product.name,
                                'product_unit_price': product.price,
                                'product_quantity': item.quantity,
                                'product_price': item.price,
                                'product_total_price': item.price * item.quantity,
                            })
                        else:
                            # Se não existe uma entrada para esse pedido, adiciona uma nova entrada à lista
                            items_dict[order_id] = {
                                'order_id': order_id,
                                'address_description': address.description,
                                'address_postal_code': address.postalCode,
                                'address_street': address.street,
                                'address_complement': address.complement,
                                'address_neighborhood': address.neighborhood,
                                'address_city': address.city,
                                'address_state': address.state,
                                'items': [{
                                    'product_name': product.name,
                                    'product_unit_price': product.price,
                                    'product_quantity': item.quantity,
                                    'product_total_price': item.price * item.quantity,
                                }]
                            }

                    # Formata o valor de order_total_price com duas casas decimais
                    order_total_price = order_total_price.quantize(Decimal('.02'),  rounding=ROUND_HALF_UP)
                    # Adiciona a somatória do preço total do pedido à entrada do pedido
                    if order_id is not None:
                        items_dict[order_id]['order_total_price'] = order_total_price

                    # Adiciona todas as entradas desse pedido à lista de resultados
                    result.extend(items_dict.values())

                except OrderItems.DoesNotExist:
                    # Se não houver itens para esse pedido, simplesmente passa para o próximo pedido
                    continue
                
            return Response(result)

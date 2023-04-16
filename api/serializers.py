from rest_framework import serializers
from api.models import *
    
class AddressSerializier(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields = '__all__'

class CategoriesSerializier(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class ProductsSerializier(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class ProductsCategoriesSerialiizer(serializers.ModelSerializer):
    class Meta:
        model = ProductsCategories
        fields = '__all__'

class OrdersSerialiizer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class OrderItemsSerialiizer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'

class CreateOrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ('orderID', 'productID', 'quantity')


class UserOrdersSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    address_description = serializers.CharField()
    address_postal_code = serializers.CharField()
    address_street = serializers.CharField()
    address_complement = serializers.CharField(allow_blank=True)
    address_neighborhood = serializers.CharField()
    address_city = serializers.CharField()
    address_state = serializers.CharField()
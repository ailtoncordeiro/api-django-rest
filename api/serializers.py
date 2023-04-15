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
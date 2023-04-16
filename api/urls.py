from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

app_name = 'API - SENAI'

router = DefaultRouter(trailing_slash=False)
router.register(r'addresses', AddressViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'products', ProductsViewSet)
router.register(r'productscategories', ProductsCategoriesViewSet)
router.register(r'orders', OrdersViewSet)
router.register(r'orderitems', OrderItemsViewSet)
#router.register(r'userorders', UserOrdersView.as_view(), basename='userorders')

urlpatterns = [
    path('addresses/userid/<int:userid>', AddressUserView.as_view()),
    path('addresses/cep/<str:cep>/', AddressCepView.as_view()),
    path('orders/user/<int:pk>', UserOrdersView.as_view()),
] + router.urls
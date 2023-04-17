from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

app_name = 'API'

router = DefaultRouter(trailing_slash=False)
router.register(r'users', UsersViewSet)

#urlpatterns = router.urls
urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # outras rotas definidas manualmente
    path('', include(router.urls)),
    # inclui as rotas do router no urlpatterns
]
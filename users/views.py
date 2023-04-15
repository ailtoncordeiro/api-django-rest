from .serializers import UsersSerializer
from .models import Users
from rest_framework import status
from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

class UsersViewSet(viewsets.ModelViewSet):

    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(description='List all users')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(description='Create a new user')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(description='Retrieve a user by ID')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(description='Update a user by ID')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(description='Delete a user by ID')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

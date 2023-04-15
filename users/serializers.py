from rest_framework import serializers
from api.models import Users

class UsersSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = [
            'id',
            'name',
            'email',
            'password'
        ]

    def create(self, validated_data):
        user = Users.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data.get('name', None),
        )
        return user
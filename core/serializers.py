from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from .models import CustomUser

class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        fields = ['email', 'username', 'password', 'first_name', 'last_name']

class UserSerializer(DjoserUserSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        fields = ['id', 'email', 'username', 'first_name', 'last_name']




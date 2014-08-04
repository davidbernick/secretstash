from rest_framework import serializers
from django.contrib.auth.models import User, Group, Permission
from rest_framework.authtoken.models import Token

from .models import Host, Secret

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name','email' )

class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('key',)


class SecretSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    content = serializers.CharField()
    read_only_fields = ('owner')

    class Meta:
        model = Secret

class HostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    apikey = TokenSerializer(required=False)
    name = serializers.CharField(max_length=100)    
    read_only_fields = ('owner')

    class Meta:
        model = Host
 
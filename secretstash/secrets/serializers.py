from rest_framework import serializers
from django.contrib.auth.models import User, Group, Permission
from rest_framework.authtoken.models import Token
from drf_compound_fields.fields import ListField

from .models import Host, Secret

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name',)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name','email',)

class UserGroupSerializer(serializers.Serializer):
    groups=ListField(serializers.CharField(),required=True)
    action = serializers.ChoiceField(choices=['add','delete'],required=True)

class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('key',)


class SecretSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    name = serializers.CharField()    
    description = serializers.CharField()
    content = serializers.CharField()
    groups=ListField(serializers.CharField(),required=False)
    
    read_only_fields = ('owner')

    class Meta:
        model = Secret
        fields = ('id', 'owner','name','description','content')

class HostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)
    apikey = TokenSerializer(required=False)
    name = serializers.CharField(max_length=100)    
    read_only_fields = ('owner')

    class Meta:
        model = Host

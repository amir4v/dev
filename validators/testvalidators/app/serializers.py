from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .validators import String, Web, Number


class UserSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(
        validators=[
            Number
        ]
    )
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

from django.contrib.auth.models import User, Group
from rest_framework import serializers

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'username')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(many = True)
    class Meta:
        model = User
        fields = ('url', 'name', 'email', 'groups')
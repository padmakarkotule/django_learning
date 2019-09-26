from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')    #('pk', 'username', 'email_id', 'created_on')


class UserSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        lookup_field= 'pk'
        fields = '__all__'

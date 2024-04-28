from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']


class PromptTextSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = PromptText
        fields = '__all__'

class PromptTextCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptText
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class UserLoginSerializer(serializers.ModelSerializer):
    class meta:
        model = User
        fields = ['username','password'] 
        # or ['email','password']
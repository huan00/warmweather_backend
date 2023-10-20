from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User
from prompt.serializers import PromptSerializer


class UserRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
                  'id',
                  'username', 
                  'password',
                  'email', 
                  'first_name', 
                  'last_name', 
                #   'address', 
                #   'city', 
                #   'state', 
                  'zip_code'
                  )
    
    def create(self, validated_data):
        print(validated_data)
        for data in validated_data:
            if data != 'password':
                validated_data[data] = validated_data[data].lower()
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserRegisterSerializer, self).create(validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    prompt = PromptSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = (
                  'id',
                  'username', 
                  'password',
                  'email', 
                  'first_name', 
                  'last_name', 
                #   'address', 
                #   'city', 
                #   'state', 
                  'zip_code',
                  'prompts'
                  )

class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

    
    class Meta:
        model = User
        fields = (
                    'id', 
                    'username',
                    'email',
                    'first_name', 
                    'last_name', 
                    # 'address', 
                    # 'city', 
                    # 'state', 
                    'zip_code'
                  )
        

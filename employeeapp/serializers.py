from rest_framework import serializers
from . models import Employee
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from djoser.serializers  import UserSerializer, UserCreateSerializer

class UserAddSerializers(serializers.ModelSerializer):
    class  Meta:
        model  =  User
        fields = ['id','first_name','last_name','email','password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, attrs):
        attrs['username'] = attrs['email']  
        return attrs

    def save(self, **kwargs):
        password = self.validated_data.get('password')
        if password:  # Check if password is provided
            self.validated_data['password'] = make_password(password)  # Hash the password using make_password
        return super().save(**kwargs)


class UserAddSerializersnew(serializers.ModelSerializer):
    class  Meta:
        model  =  User
        fields = ['id','first_name','last_name','email']
        


class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields= ['phone','designation','company']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username',  'email', 'first_name', 'last_name',]
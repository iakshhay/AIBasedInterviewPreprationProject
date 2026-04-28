from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','first_name','last_name','created_at','updated_at']
        read_only_fields=['id','created_at','updated_at']

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,min_length=8,required=True)
    class Meta:
        model=User
        fields=['email','password','first_name','last_name']

    def validate_email(self,value):
        value=value.strip().lower()
        if User.objects.filter(email=value).exists():
            raise ValidationError("This email is already taken.")
        return value

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['email','password']

    def validate(self, data):
        email=data.get('email','')
        password=data.get('password')

        if not email or not password:
            raise ValidationError("Email and password are required")

        email=email.strip().lower()
        user = authenticate(username=email,password=password)

        if user is None:
            raise ValidationError("Invalid credentials")
        
        if not user.is_active:
            raise ValidationError("User account is disabled")
        
        data['user']=user
        return data
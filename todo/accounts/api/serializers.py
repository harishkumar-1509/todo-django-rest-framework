from rest_framework import serializers
from ..models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from ..utils import *

class UserRegistrationSerializer(serializers.ModelSerializer):
    # We are writing this because we need to confirm the password2 
    password2 = serializers.CharField(style={'input_type':'password'}, write_only = True)
    class Meta:
        model = User
        fields = ['email', 'name', 'mobile_number', 'country_code', 'date_of_birth', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only':True}
        } 
    
    # Object level validation
    def validate(self, obj):
        password = obj.get('password')
        password2 = obj.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and confirm password doesn't match")
        return obj
    
    # We are adding this because we are performing operation on a custom model
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

class UserLoginSerilaizer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']

class UserProfileSerilaizer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['name','email','mobile_number','country_code','date_of_birth']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    
    class Meta:
        fields = ['password','password2']
    
    def validate(self, obj):
        password = obj.get('password')
        password2 = obj.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and confirm password doesn't match")
        user.set_password(password)
        user.save()
        return obj

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    
    class Meta:
        fields = ['email']
    
    def validate(self, obj):
        email = obj.get('email')
        if User.objects.get(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            # Client side url
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            # Send email here
            body = 'Click Following Link to Reset Your Password' + link
            data = {
                "subject":"Reset your password",
                "body":body,
                'to_email': user.email,
            }
            Util.send_email(data)
            return obj
        else:
            raise serializers.ValidationError("You are not a registered user")

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    
    class Meta:
        fields = ['password','password2']
    
    def validate(self, obj):
        try:
            password = obj.get('password')
            password2 = obj.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and confirm password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError("Token is not valid or expired!")
            user.set_password(password)
            user.save()
            return obj
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError("Token is not valid or expired!")

        
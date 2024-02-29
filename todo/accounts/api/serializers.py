from rest_framework import serializers
from ..models import User

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
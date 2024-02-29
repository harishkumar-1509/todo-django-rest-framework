from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from ..renderers import *
from rest_framework_simplejwt.tokens import RefreshToken

# Generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationAPIView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            data = {
                'msg':'Registration success', 
                'value': None,
                'token': token
            }
            return Response(status = status.HTTP_201_CREATED, data = data)
        else:
            data = {
                    'msg':'Something went wrong in registration', 
                    'value': serializer.errors
                }
            return Response(data = data, status=status.HTTP_400_BAD_REQUEST,)

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request):
        serailizer = UserLoginSerilaizer(data = request.data)
        if serailizer.is_valid():
            email = serailizer.data.get('email')
            password = serailizer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                data = {
                'msg': 'Login success', 
                'value': user,
                'token': token
                }
                return Response(data = data, status=status.HTTP_200_OK)
            else:
                data = {
                'msg': 'Error or password is not valid', 
                'value':None
                }
                return Response(data = data, status=status.HTTP_404_NOT_FOUND)
        data = {
                'msg': 'Something went wrong while logging in', 
                'value':serailizer.errors
                }
        return Response(data = data, status=status.HTTP_200_OK)
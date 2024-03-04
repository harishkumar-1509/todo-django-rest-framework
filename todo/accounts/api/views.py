from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from ..renderers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

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
                'msg':'Registration success, Please login with these credentials!', 
                'value': None,
                'token': token
            }
            return Response(status = status.HTTP_201_CREATED, data = data)
        else:
            data = {
                    'msg':'Something went wrong in registration!', 
                    'value': serializer.errors,
                    'token': None
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
                logged_in_user = User.objects.get(email = str(user))
                logged_in_user_details = {
                    'email': logged_in_user.email,
                    'name': logged_in_user.name,
                    'mobile_number': logged_in_user.mobile_number,
                    'country_code': logged_in_user.country_code,
                    'date_of_birth': logged_in_user.date_of_birth.isoformat()
                }
                data = {
                'msg': 'Login success', 
                'value': logged_in_user_details,
                'token': token
                }
                return Response(data = data, status=status.HTTP_200_OK)
            else:
                data = {
                'msg': 'Error or password is not valid', 
                'value':None,
                'token': None
                }
                return Response(data = data, status=status.HTTP_404_NOT_FOUND)
        data = {
                'msg': 'Something went wrong while logging in', 
                'value':serailizer.errors,
                'token': None
                }
        return Response(data = data, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        serializer = UserProfileSerilaizer(request.user)
        data = {
                'msg': 'Fetched the user details', 
                'value':serializer.data,
                'token': None
                }
        return Response(data = data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data, context = {'user': request.user})
        if serializer.is_valid():
            data = {
                'msg': 'Password changed successfully', 
                'value':None,
                'token': None
                }
            return Response(data = data, status=status.HTTP_200_OK)
        data = {
                'msg': 'Something went wrong while changing password', 
                'value':serializer.errors,
                'token': None
                }
        return Response(data = data, status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self,request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid():
            data = {
                'msg': 'Password reset link sent to your email, please check', 
                'value':None,
                'token': None
                }
            return Response(data = data, status=status.HTTP_200_OK)
        data = {
                'msg': 'Something went wrong while sendind the email, please try after sometime!', 
                'value':serializer.errors,
                'token': None
                }
        return Response(data = data, status=status.HTTP_400_BAD_REQUEST)

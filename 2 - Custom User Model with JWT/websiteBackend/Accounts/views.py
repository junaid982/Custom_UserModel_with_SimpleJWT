from django.shortcuts import render
from django.contrib.auth import authenticate  #for user authentication 

from .models import MyUser
from .serializers import MyUserSerializers

from rest_framework.decorators import APIView
from rest_framework import status
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.



# generate Tokens manually 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserLoginView(APIView):
    
    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            
            token = get_tokens_for_user(user)

            return Response({'msg': 'Login Successful', 'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Email or password Not Valid'}, status=status.HTTP_404_NOT_FOUND)

class RegisterUserView(APIView):
    def post(self, request, format=None):
        serializer = MyUserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Registered successfully.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
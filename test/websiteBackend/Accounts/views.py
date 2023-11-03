from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer , UserLoginSerializer 
from django.contrib.auth import authenticate  #for user authentication 
# from accounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import User


from rest_framework import status, viewsets
from rest_framework.decorators import action

from django.contrib.auth.models import User as UserPass

# generate Tokens manually 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



# User Registration view  
class RegisterUserView(APIView):
    # permission_classes = [IsAuthenticated]
  
    
    def post(self , request , format=None):
        #print("Data :",request.data)
        serializer = UserRegistrationSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

            # generating tokens for new registered user
        # token = get_tokens_for_user(user) 

        return Response({"msg":"Registration Successful"} , status=status.HTTP_201_CREATED)
        

# User Login View 
class UserLoginView(APIView):
    
    
    def post(self , request , format=None):
    
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(email = email , password = password)
        if user is not None: 

            # generating tokens for login user
            token = get_tokens_for_user(user)    
            # print('request.user.is_admin :',serializer.data.get('is_admin'))

            # print('serializer.data :',serializer.data)

            return Response({'token':token ,'msg':'Login Successful' } , status=status.HTTP_200_OK)
        else:
            return Response( {'errors':{'non_field_errors':['Email or password Not Valid']} },status=status.HTTP_404_NOT_FOUND)

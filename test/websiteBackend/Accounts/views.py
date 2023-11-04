from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer , UserLoginSerializer ,UserSerializer
from django.contrib.auth import authenticate , login #for user authentication 
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

        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.data.get('email' , None)
            password = serializer.data.get('password' , None)
            
            user = authenticate(email = email , password = password)
            if user is not None: 
                login(request, user) # update last login details
                token = get_tokens_for_user(user)
                data = User.objects.get(email = email)
                userDetails = UserSerializer(data , context = {'request' : request})
                userDetails.data.pop('password', None)
                
                return Response({'msg':'Login Successful' ,'token':token , "userDetails" : userDetails.data} , status=status.HTTP_200_OK)

            else:
                return Response( {'error':'Email or password Not Valid' },status=status.HTTP_404_NOT_FOUND)
            
        return Response( {'errors': serializer.errors },status=status.HTTP_404_NOT_FOUND)
    

class GetAllUsers(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        all_users = User.objects.all()
        serializer =  UserSerializer(all_users , many = True , context = {'request':request})

        return Response({"all_users" : serializer.data })

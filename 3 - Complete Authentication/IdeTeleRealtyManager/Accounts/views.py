
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.views import APIView
from django.contrib.auth import authenticate  #for user authentication 
# from accounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserRegistrationSerializer , UserLoginSerializer ,GetUserDetailsSerializers , UpdateUserDetailsByAdminSerializer ,ChangeUserPasswordAdminAccessSerializer

from rest_framework import status, viewsets
from rest_framework.decorators import action

from django.contrib.auth.models import User as UserPass
import os


# generate Tokens manually 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



# User Registration view  
class UserRegistrationView(APIView):
    # permission_classes = [IsAuthenticated]
  
    
    def post(self , request , format=None):
        try:
            #print("Data :",request.data)
            serializer = UserRegistrationSerializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

                # generating tokens for new registered user
            # token = get_tokens_for_user(user) 

            return Response({"message":"Registration Successful"} , status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"error" : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# User Login View 
class UserLoginView(APIView):
    
    
    def post(self , request , format=None):
        try:
    
            email = request.data.get('email',None)
            password = request.data.get('password' , None)

            try:
                email_Check = User.objects.get(email = email )

            except:
                return Response( {'error':'Email not exists'},status=status.HTTP_404_NOT_FOUND)
            
            user = authenticate(email = email , password = password)
            if user is not None: 

                # generating tokens for login user
                token = get_tokens_for_user(user)    
                serializer = GetUserDetailsSerializers( email_Check , context = {'request':request})

                # print(serializer.data)

                return Response({'token':token ,"user_data" : serializer.data ,'msg':'Login Successful' } , status=status.HTTP_200_OK)
            else:
                return Response( {'error':'Invalid password'},status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error" : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Get All User Details        
class GetAllUserDetails(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        try:
            users = User.objects.all()
            serializer = GetUserDetailsSerializers(users, many=True , context = {'request':request})

            return Response(serializer.data , status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error" : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Get User Details By id
class GetUserDetailsById(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self , request ,pk=None ,format=None):
        try:
                

            # email = request.data.get("email" , None)
            try:
                email_Check = User.objects.get(id = pk )

            except:
                return Response( {'error':'Email not exists'},status=status.HTTP_404_NOT_FOUND)
            
            serializer =  GetUserDetailsSerializers( email_Check , context = {'request':request})

            return Response(serializer.data , status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error" : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Edit User Details and Permissions
class EditUserDetailsView(APIView):
    # permission_classes = [IsAuthenticated]

    def patch(self , request ,pk = None , format=None):

        try:

            data = request.data
            try:
                user = User.objects.get(id = pk)
            except:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = UpdateUserDetailsByAdminSerializer(user, data=request.data, partial=True, context={"request": request})
            if serializer.is_valid():
            
                new_profile_image = data.get('user_profile' , None)
                current_profile = user.user_profile.path if user.user_profile else None 

                if current_profile != "default_profile/avatar.webp":
                    if current_profile:
                        try:
                            os.remove(current_profile)
                        except FileNotFoundError:
                            pass
                
                serializer.save()
                return Response( serializer.data, status=status.HTTP_200_OK)
            
            return Response({"error": serializer.errors }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error" : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Change User Password  By Admin
class ChangeUserPasswordView(APIView):
    # permission_classes = [IsAuthenticated]

    def patch(self, request, pk = None ):
        try:
            user = User.objects.get(id = pk)
        except:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # user = User.objects.get(id = pk)
        serializer = ChangeUserPasswordAdminAccessSerializer(data=request.data)

        if serializer.is_valid():
            new_password = serializer.validated_data['password']
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RemoveUser_View(APIView):
    # permission_classes = [IsAuthenticated]

    def delete(self , request , pk = None , format=None):

        try:

            try:
                user = User.objects.get(id = pk)
            except:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            user.delete()

            return Response({"message" : "User Remove from our Panel"} , status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error" : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
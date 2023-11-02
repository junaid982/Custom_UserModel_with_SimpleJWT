from rest_framework import serializers
from .models import User 

# import for send reset password email
from django.utils.encoding import smart_str ,force_bytes , DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.contrib.auth import get_user_model
# from accounts.utils import Util



# Create a serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'designation', 'is_admin' ,'is_active', 'is_staff', 'created_at', 'updated_at')



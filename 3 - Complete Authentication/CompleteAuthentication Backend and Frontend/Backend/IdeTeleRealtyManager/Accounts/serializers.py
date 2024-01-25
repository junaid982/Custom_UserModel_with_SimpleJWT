from rest_framework import serializers
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'name', 'designation', 'user_roll', 'password', 'user_profile']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create_user(**validated_data, password=password)
        return user
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                if user.check_password(password):
                    return data
            raise serializers.ValidationError("Invalid email or password")
        raise serializers.ValidationError("Both email and password are required")


class GetUserDetailsSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password']



class UpdateUserDetailsByAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name' , "designation" , "user_roll" , "user_profile" ,  "is_active" , "is_admin" , "dashboard_perms" , "sheets_perms" , "uploads_perms" , "users_perms" , "activity_perms" , "other_perms")


    def update(self, instance, validated_data):
    
        instance.name = validated_data.get('name', instance.name)
        instance.designation = validated_data.get('designation', instance.designation)
        instance.user_roll = validated_data.get('user_roll', instance.user_roll)
        instance.user_profile = validated_data.get('user_profile', instance.user_profile)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_admin = validated_data.get('is_admin', instance.is_admin)
        instance.dashboard_perms = validated_data.get('dashboard_perms', instance.dashboard_perms)
        instance.sheets_perms = validated_data.get('sheets_perms', instance.sheets_perms)
        instance.uploads_perms = validated_data.get('uploads_perms', instance.uploads_perms)
        instance.users_perms = validated_data.get('users_perms', instance.users_perms)
        instance.activity_perms = validated_data.get('activity_perms', instance.activity_perms)
        instance.other_perms = validated_data.get('other_perms', instance.other_perms)
        
        instance.save()

        return instance
    

# Change User password by admin 
class ChangeUserPasswordAdminAccessSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)
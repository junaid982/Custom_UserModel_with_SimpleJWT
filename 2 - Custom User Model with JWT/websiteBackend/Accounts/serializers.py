from rest_framework import serializers
# from .models import MyUser
from django.contrib.auth import get_user_model

class MyUserSerializers(serializers.ModelSerializer):

    class Meta:
        # model = MyUser
        model = get_user_model()
        fields = "__all__"



from django.urls import path
from .views import UserLoginView ,UserRegistrationView  ,GetAllUserDetails,GetUserDetailsById ,EditUserDetailsView ,ChangeUserPasswordView , RemoveUser_View

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('user-login/' , UserLoginView.as_view()),
    path('register-user/' , UserRegistrationView.as_view()),
    path('token/refresh/' , TokenRefreshView.as_view() , name="refresh"),

    path('get/all-user/details/' , GetAllUserDetails.as_view()),
    path('get/user/details/by/<int:pk>/' , GetUserDetailsById.as_view()),
    path('edit/user/details/by/admin/<int:pk>/' , EditUserDetailsView.as_view()),
    path('change/user/password/by/admin/<int:pk>/' , ChangeUserPasswordView.as_view()), 
    path('remove/user/by/admin/<int:pk>/' , RemoveUser_View.as_view()), 
]
from django.urls import path
from . import views

urlpatterns = [
    path('user-login/' , views.UserLoginView.as_view()),
    path('register-user/' , views.RegisterUserView.as_view()), 
    path('get/all-users/' , views.GetAllUsers.as_view()),
]


(switch git into code mode mode )

These are the steps to create Custom user model in Djnago

reference custom user model
(AbstractBaseUser)

https://docs.djangoproject.com/en/4.2/topics/auth/customizing/



required Libraries in global enviroment 


Windows 
pip install django 
pip install virtualenv 


Linux 
sudo apt install python3-pip 
pip install django
sudo pip install virtualenv


---------------------------------------------------------------------------------------
Step 1 

Create Django project 

>>> django-admin startproject websiteBackend

>>> cd websiteBackend

---------------------------------------------------------------------------------------
Step 2 

create virtual enviroment and install Libraries 

windows
>>> virtualenv env 

activate enviroment
>>>env\Scripts\activate


Linux
>>> virtualenv env

activate enviroment 
>>>source env/bin/activate



>>> pip install django
>>> pip install djangorestframework

---------------------------------------------------------------------------------------
Step 3

Create django app

>>> python manage.py startapp Accounts

---------------------------------------------------------------------------------------
Step 4

Open Vs code 

>>> code .


---------------------------------------------------------------------------------------
Step 5

install rest_framework and application in settings.py 


open settings.py 


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'Accounts',
]


---------------------------------------------------------------------------------------

Step 6

setup media directory and static directory 

=> open settings.py  

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


=> and open urls.py ( project )

from django.contrib import admin
from django.urls import path
from django.conf import settings                # import for setup media and static
from django.conf.urls.static import static      # import for setup media and static

urlpatterns = [
    path('admin/', admin.site.urls),
    
]

# add this line 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL , document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)

---------------------------------------------------------------------------------------

Step 7

create custom user model and UserManager
add fields according to your requirements 

models.py ( Accounts App )

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, email,name , designation,user_roll, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name = name,
            designation = designation,
            user_roll = user_roll,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, designation , user_roll , password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            designation = designation,
            user_roll = user_roll,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    user_roll = models.CharField(max_length=255)

    profile_image = models.ImageField(upload_to='Profile_image/' , null=True , blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name" , "designation" , 'user_roll']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


---------------------------------------------------------------------------------------

Step 8 

Setup admin.py ( Accounts App )

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from Accounts.models import MyUser


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "name","designation","user_roll","profile_image" ,"is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name","designation" , "user_roll" , "profile_image"]}),
        ("Permissions", {"fields": ["is_admin","is_active"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


---------------------------------------------------------------------------------------

Step 9 

register custom user model in a settings.py 
and add this line below databse settings

open settings.py 

AUTH_USER_MODEL = "Accounts.MyUser"



---------------------------------------------------------------------------------------

Step 10 

open terminal and enter these commands 

>>> python manage.py makemigrations
>>> python manage.py migrate
>>> python manage.py createsuperuser


---------------------------------------------------------------------------------------

Step 11 

goto 

http://127.0.0.1:8000/admin


login and custom user Model complete 


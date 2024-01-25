from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, name, designation, user_roll, user_profile=None, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            designation=designation,
            user_roll=user_roll,
            user_profile=user_profile
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, designation, user_roll, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name,
            designation=designation,
            user_roll=user_roll,
        )
        user.is_admin = True
        user.dashboard_perms = True
        user.sheets_perms = True
        user.uploads_perms = True
        user.users_perms = True
        user.activity_perms = True

        user.save(using=self._db)
        return user
   

    


# First create Our custom user model .
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email Address",
        max_length=255,
        unique=True,
    )
    
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    user_roll = models.CharField(max_length=255)
    # user_profile = models.ImageField(upload_to='User_Profile/', default='Default_Profile/avatar.webp')
    user_profile = models.ImageField(upload_to='User_profile/', default='Default_profile/avatar.webp')
    # Add or modify fields as per your requirements

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # Permissions
    dashboard_perms = models.BooleanField(default=False)
    sheets_perms = models.BooleanField(default=False)
    uploads_perms = models.BooleanField(default=False)
    users_perms = models.BooleanField(default=False)
    activity_perms = models.BooleanField(default=False)
    other_perms = models.JSONField(null=True, default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    # Your UserManager definition
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "designation", "user_roll"]

    # for default user profile 
    def save(self, *args, **kwargs):
        if not self.user_profile:
            self.user_profile = 'Default_profile/avatar.webp'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

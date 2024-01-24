
from django.contrib import admin
from . models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class UserModelAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.

    list_display = ["id" , "email", "name", "is_admin" ,"dashboard_perms", "sheets_perms" ,"uploads_perms" ,"users_perms" ,"activity_perms" ,"other_perms" ,"user_profile" , "created_at" , "updated_at"]
    list_filter = ["is_admin"]
    fieldsets = [
        ('User Credentials', {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name" , "designation" ,"user_profile"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name" , "designation", "password"],
            },
        ),
    ]
    search_fields = ["email" , "name"]
    ordering = ["email" , "id"]
    filter_horizontal = []

# Now register the new UserAdmin...
admin.site.register(User, UserModelAdmin)

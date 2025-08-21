from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ['-created_at']
    list_display = ['email', 'username', 'phone_number', 'is_staff', 'is_rider', 'is_superuser', 'is_verified']
    list_filter = ['is_staff', 'is_rider', 'is_superuser', 'is_verified']

admin.site.register(User, UserAdmin)

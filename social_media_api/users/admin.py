from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Import your custom User model

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('email',)

admin.site.register(User, UserAdmin)  # Register the custom User model

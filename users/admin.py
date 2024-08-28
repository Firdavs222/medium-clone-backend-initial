from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

@admin.register(CustomUser)

class CustomUserAdmin(UserAdmin):  
    """fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('middle_name',)}),
    )"""
    fieldsets = UserAdmin.fieldsets + (
        ('Additional info', {
            'fields': ('middle_name', 'avatar',)
        }),
    )
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'middle_name')
    list_display_links = ('id', 'username', 'email')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'middle_name')
    list_filter = ('last_login', 'date_joined', 'is_staff', 'is_superuser', 'is_active')

# admin.site.register(CustomUser, CustomUserAdmin)
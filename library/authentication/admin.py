from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    ordering = ('id',)
    filter_horizontal = ()

    fieldsets = (
        ('Login Information', {
            'fields': ('email', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'middle_name')
        }),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_superuser')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2', 'role', 'is_active')
        }),
    )
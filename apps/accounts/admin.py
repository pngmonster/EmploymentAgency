from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ('email', 'role', 'is_verified', 'is_active', 'created_at')
    list_filter   = ('role', 'is_verified', 'is_active')
    search_fields = ('email',)
    ordering      = ('-created_at',)

    fieldsets = (
        (None,           {'fields': ('email', 'password')}),
        ('Роль',         {'fields': ('role', 'is_verified')}),
        ('Права',        {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты',         {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    readonly_fields  = ('last_login', 'created_at', 'updated_at')
    add_fieldsets    = (
        (None, {
            'classes': ('wide',),
            'fields':  ('email', 'role', 'password1', 'password2'),
        }),
    )

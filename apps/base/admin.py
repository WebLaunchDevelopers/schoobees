from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class CustomUserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'school_name', 'country', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('school_name', 'country', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'register_id')}),
        (_('Personal info'), {'fields': ('school_name', 'chairman', 'principal', 'email', 'mobile_number', 'address', 'country')}),
        (_('Permissions'), {'fields': ('approved', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'chairman', 'principal', 'email', 'password1', 'password2', 'school_name', 'mobile_number', 'country', 'address'),
        }),
    )
    
    def school_name(self, obj):
        return obj.userprofile.school_name
    
    def country(self, obj):
        return obj.userprofile.country


admin.site.register(CustomUser, CustomUserAdmin)

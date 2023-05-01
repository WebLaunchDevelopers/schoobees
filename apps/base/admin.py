from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserProfile
from apps.staffs.models import Staff


class UserProfileInline(admin.StackedInline):
    model = UserProfile
class StaffInline(admin.StackedInline):
    model = Staff

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_faculty', 'is_superuser')
    list_filter = ('userprofile__school_name', 'userprofile__country', 'is_active', 'is_faculty', 'is_superuser')
    fieldsets = (
            (None, {'fields': ('username', 'password', 'register_id')}),
            (_('Personal info'), {'fields': ('email',)}),
            (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'is_faculty','approved')}),
            (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_faculty'),
        }),
    )

    def get_inline_instances(self, request, obj=None):
        if obj and not obj.is_faculty:
            inlines = [UserProfileInline]
        else:
            inlines = []
        return [inline(self.model, self.admin_site) for inline in inlines]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # replace this with your custom logic to exclude the specific users
        excluded_users = CustomUser.objects.filter(username__in=['admin1', 'admin2'])
        return qs.exclude(pk__in=excluded_users)

admin.site.register(CustomUser, CustomUserAdmin)

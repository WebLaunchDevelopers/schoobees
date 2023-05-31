from django.contrib import admin
from .models import Staff

class StaffAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'current_status')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('current_status',)
    readonly_fields = ('temp_password',)
    
    class Meta:
        model = Staff

admin.site.register(Staff, StaffAdmin)
